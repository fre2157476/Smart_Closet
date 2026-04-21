import streamlit as st
from services.api import upload_clothing

def show_upload_page():
    st.title("Upload Clothing Item")

    user_id = st.session_state.get("user_id")
    if user_id is None:
        st.error("User not logged in.")
        return

    with st.form("upload_clothing_form"):
        uploaded_file = st.file_uploader(
            "Choose clothing image",
            type=["jpg", "jpeg", "png"]
        )

        col1, col2 = st.columns(2)

        with col1:
            item_name = st.text_input("Item Name",
                                      placeholder="Ex: Christmas Shirt")
            category = st.selectbox(
                "Category (optional)",
                ["", "top", "bottom", "footwear", "dress", "outerwear"],
                placeholder="Optional: AI can help detect this"
            )
            subcategory = st.text_input(
                "Subcategory",
                placeholder="Optional: AI can help detect this"
            )

        with col2:
            color = st.text_input(
                "Color",
                placeholder="Optional: auto-detected if left blank"
            )
            season = st.selectbox(
                "Season (optional)",
                ["", "Spring", "Summer", "Fall", "Winter", "All Season"]
            )
            occasion = st.selectbox(
                "Occasion (optional)",
                ["", "Casual", "Formal", "Business", "Sport", "Party", "Travel"]
            )

        st.caption("Leave category, subcategory, or color blank if you want the system to detect them automatically.")

        submit = st.form_submit_button("Upload Item")

    if submit:
        if uploaded_file is None:
            st.error("Please choose an image file.")
            return

        result = upload_clothing(
            file=uploaded_file,
            user_id=user_id,
            item_name=item_name,
            category=category,
            subcategory=subcategory,
            color=color,
            season=season,
            occasion=occasion
        )

        if result:
            st.success("Clothing item uploaded successfully!")

            st.subheader("Saved Item Details")
            st.write(f"**Item Name:** {result.get('item_name') or 'Unnamed Item'}")
            st.write(f"**Category:** {result.get('category') or 'N/A'}")
            st.write(f"**Subcategory:** {result.get('subcategory') or 'N/A'}")
            st.write(f"**Color:** {result.get('color') or 'N/A'}")
            st.write(f"**Season:** {result.get('season') or 'N/A'}")
            st.write(f"**Occasion:** {result.get('occasion') or 'N/A'}")
        else:
            st.error("Upload failed.")