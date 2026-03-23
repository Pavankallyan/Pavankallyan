import streamlit as st
import torch
import torch.nn as nn
from torchvision import transforms, models
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from PIL import Image
import numpy as np

# Page config
st.set_page_config(
    page_title="Pneumonia Detector",
    page_icon="🫁",
    layout="centered"
)

# Load model
@st.cache_resource
def load_model():
    device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')

    def build_resnet50():
        model = models.resnet50(weights=None)
        in_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(512, 2)
        )
        return model

    model = build_resnet50().to(device)
    model.load_state_dict(torch.load(
        '../models/best_resnet50.pth',
        map_location=device
    ))
    model.eval()
    return model, device

# Preprocess image
def preprocess(img_pil):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    return transform(img_pil).unsqueeze(0)

# Generate Grad-CAM
def generate_gradcam(model, input_tensor, img_pil, device):
    target_layers = [model.layer4[-1]]
    cam = GradCAM(model=model, target_layers=target_layers)
    img_np = np.array(img_pil.resize((224, 224))) / 255.0
    grayscale_cam = cam(input_tensor=input_tensor.to(device))[0]
    visualization = show_cam_on_image(
        img_np.astype(np.float32), grayscale_cam, use_rgb=True
    )
    return visualization

# UI
st.title("Pneumonia Detection from Chest X-rays")
st.markdown("Upload a chest X-ray and the model will predict whether it shows **NORMAL** lungs or **PNEUMONIA**, with a Grad-CAM heatmap showing what the model focused on.")

st.divider()

uploaded_file = st.file_uploader(
    "Upload a chest X-ray image",
    type=['jpg', 'jpeg', 'png']
)

if uploaded_file is not None:
    img_pil = Image.open(uploaded_file).convert('RGB')

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original X-ray")
        st.image(img_pil, use_container_width=True)

    with st.spinner("Analyzing X-ray..."):
        model, device = load_model()
        input_tensor  = preprocess(img_pil).to(device)

        with torch.no_grad():
            output     = model(input_tensor)
            probs      = torch.softmax(output, dim=1)[0]
            pred       = output.argmax(1).item()
            confidence = probs[pred].item() * 100

        pred_label = "PNEUMONIA" if pred == 1 else "NORMAL"
        gradcam_img = generate_gradcam(model, input_tensor, img_pil, device)

    with col2:
        st.subheader("Grad-CAM Heatmap")
        st.image(gradcam_img, use_container_width=True)

    st.divider()
    st.subheader("Prediction Result")

    if pred_label == "PNEUMONIA":
        st.error(f"PNEUMONIA detected — Confidence: {confidence:.1f}%")
    else:
        st.success(f"NORMAL lungs — Confidence: {confidence:.1f}%")

    col3, col4 = st.columns(2)
    with col3:
        st.metric("NORMAL probability",    f"{probs[0].item()*100:.1f}%")
    with col4:
        st.metric("PNEUMONIA probability", f"{probs[1].item()*100:.1f}%")

    st.divider()
    st.caption("Built with PyTorch + ResNet50 + Grad-CAM | Master's ML Project")