import streamlit as st
from app.auth import login_user, get_current_user
from app.image_manager import get_random_untagged_image
from app.redis_client import store_classification, CLASS_LABELS
from app.state import get_state, set_state
import os


def main():
    st.set_page_config(page_title="Image Tagger", layout="centered")

    user = get_current_user()
    if not user:
        login_user()
        return

    current_image = get_state("current_image", get_random_untagged_image(user))
    if not current_image:
        st.title(f"Hola, {user}!")
        st.info("🎉 No quedan imágenes para clasificar.")
        return

    st.title(f"Hola, {user}! Clasificá la imagen")
    st.image(
        current_image, use_container_width=True, caption=os.path.basename(current_image)
    )

    st.markdown("---")

    # Initialize selection state
    if "dropdown_selection" not in st.session_state:
        st.session_state.dropdown_selection = "-- Elegir --"

    # Dropdown
    st.session_state.dropdown_selection = st.selectbox(
        "Seleccioná la clase",
        options=["-- Elegir --"] + CLASS_LABELS,
        index=(
            0
            if st.session_state.dropdown_selection == "-- Elegir --"
            else CLASS_LABELS.index(st.session_state.dropdown_selection) + 1
        ),
        key="dropdown_widget",
    )

    # Confirm
    if st.session_state.dropdown_selection != "-- Elegir --":
        if st.button("✅ Confirmar clasificación"):
            store_classification(
                user=user,
                image_name=os.path.basename(current_image),
                label=st.session_state.dropdown_selection,
            )
            set_state("current_image", get_random_untagged_image(user))
            st.session_state.dropdown_selection = "-- Elegir --"
            st.rerun()


if __name__ == "__main__":
    main()
