import streamlit as st
from pathlib import Path
from services.api import get_clothes, delete_clothing_item
from services.api import save_outfit, update_clothing_item


def show_closet_page():
    st.title("My Closet")

    if "outfit_success" in st.session_state:
        st.success(st.session_state["outfit_success"])

    user_id = st.session_state.get("user_id")
    if user_id is None:
        st.error("User not logged in.")
        return

    if "outfit_items" not in st.session_state:
        st.session_state["outfit_items"] = []

    if "editing_item_id" not in st.session_state:
        st.session_state["editing_item_id"] = None

    clothes = get_clothes(user_id)

    if not clothes:
        st.info("No clothing items yet.")
        return

    project_root = Path(__file__).resolve().parents[2]
    uploads_dir = project_root / "src" / "uploads"

    categories = ["All"] + sorted(
        {item.get("category") for item in clothes if item.get("category")}
    )
    colors = ["All"] + sorted(
        {item.get("color") for item in clothes if item.get("color")}
    )

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        selected_category = st.selectbox("Filter by Category", categories)

    with filter_col2:
        selected_color = st.selectbox("Filter by Color", colors)

    filtered_clothes = clothes

    if selected_category != "All":
        filtered_clothes = [
            item for item in filtered_clothes
            if item.get("category") == selected_category
        ]

    if selected_color != "All":
        filtered_clothes = [
            item for item in filtered_clothes
            if item.get("color") == selected_color
        ]

    st.subheader("Clothing Items")

    cols = st.columns(3)

    for i, item in enumerate(filtered_clothes):
        col = cols[i % 3]

        with col:
            image_url = item.get("image_url")
            if image_url:
                filename = Path(image_url).name
                real_image_path = uploads_dir / filename

                if real_image_path.exists():
                    st.image(str(real_image_path), width=180)
                else:
                    st.warning("Image not found")

            st.caption(item.get("item_name") or "Unnamed Item")
            st.write(f"Category: {item.get('category') or 'N/A'}")
            st.write(f"Subcategory: {item.get('subcategory') or 'N/A'}")
            st.write(f"Color: {item.get('color') or 'N/A'}")
            st.write(f"Season: {item.get('season') or 'N/A'}")
            st.write(f"Occasion: {item.get('occasion') or 'N/A'}")

            btn_col1, btn_col2 = st.columns(2)

            with btn_col1:
                if st.button("Add to Outfit", key=f"add_{item.get('id', i)}"):
                    already_added = any(
                        outfit_item.get("id") == item.get("id")
                        for outfit_item in st.session_state["outfit_items"]
                    )

                    if not already_added:
                        st.session_state["outfit_items"].append(item)
                        st.rerun()

            with btn_col2:
                if st.button("Edit", key=f"edit_{item.get('id', i)}"):
                    st.session_state["editing_item_id"] = item.get("id")
                    st.rerun()

            if st.button("Delete", key=f"delete_{item.get('id', i)}"):
                result = delete_clothing_item(item.get("id"))
                if result:
                    st.success("Item deleted successfully!")
                    if st.session_state["editing_item_id"] == item.get("id"):
                        st.session_state["editing_item_id"] = None
                    st.rerun()
                else:
                    st.error("Failed to delete item")

    editing_item_id = st.session_state.get("editing_item_id")

    if editing_item_id:
        item_to_edit = next(
            (item for item in clothes if item.get("id") == editing_item_id),
            None
        )

        if item_to_edit:
            st.subheader("Edit Item")

            with st.form("edit_item_form"):
                edit_item_name = st.text_input(
                    "Item Name",
                    value=item_to_edit.get("item_name") or ""
                )

                edit_category = st.text_input(
                    "Category",
                    value=item_to_edit.get("category") or ""
                )

                edit_subcategory = st.text_input(
                    "Subcategory",
                    value=item_to_edit.get("subcategory") or ""
                )

                edit_color = st.text_input(
                    "Color",
                    value=item_to_edit.get("color") or ""
                )

                edit_season = st.text_input(
                    "Season",
                    value=item_to_edit.get("season") or ""
                )

                edit_occasion = st.text_input(
                    "Occasion",
                    value=item_to_edit.get("occasion") or ""
                )

                form_col1, form_col2 = st.columns(2)

                with form_col1:
                    save_changes = st.form_submit_button("Save Changes")

                with form_col2:
                    cancel_edit = st.form_submit_button("Cancel")

            if save_changes:
                result = update_clothing_item(
                    item_id=editing_item_id,
                    item_name=edit_item_name,
                    category=edit_category,
                    subcategory=edit_subcategory,
                    color=edit_color,
                    season=edit_season,
                    occasion=edit_occasion,
                )

                if result:
                    st.success("Item updated successfully!")
                    st.session_state["editing_item_id"] = None
                    st.rerun()
                else:
                    st.error("Update failed.")

            if cancel_edit:
                st.session_state["editing_item_id"] = None
                st.rerun()

    st.subheader("Current Outfit")

    outfit_items = st.session_state.get("outfit_items", [])

    if not outfit_items:
        st.info("No items added to outfit yet.")
    else:
        outfit_cols = st.columns(4)

        for i, item in enumerate(outfit_items):
            col = outfit_cols[i % 4]

            with col:
                image_url = item.get("image_url")
                if image_url:
                    filename = Path(image_url).name
                    real_image_path = uploads_dir / filename

                    if real_image_path.exists():
                        st.image(str(real_image_path), width=140)

                st.caption(item.get("item_name") or "Unnamed Item")

                if st.button("Remove", key=f"remove_{item.get('id', i)}"):
                    st.session_state["outfit_items"] = [
                        outfit_item
                        for outfit_item in st.session_state["outfit_items"]
                        if outfit_item.get("id") != item.get("id")
                    ]
                    st.rerun()

        if st.button("Clear Outfit"):
            st.session_state["outfit_items"] = []
            st.rerun()

        st.subheader("Save Outfit")

        outfit_name = st.text_input("Outfit Name")

        if st.button("Save Outfit"):
            if not outfit_name.strip():
                st.error("Enter an outfit name.")
            else:
                clothing_item_ids = [
                    item["id"]
                    for item in outfit_items
                    if item.get("id") is not None
                ]

                result = save_outfit(user_id, outfit_name, clothing_item_ids)


                if result:
                    st.session_state["outfit_success"] = "Outfit saved successfully!"
                    st.session_state["outfit_items"] = []
                    st.rerun()
                else:
                    st.error("Failed to save outfit.")