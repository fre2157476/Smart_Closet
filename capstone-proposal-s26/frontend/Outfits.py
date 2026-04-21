import streamlit as st
from pathlib import Path
from services.api import get_saved_outfits, delete_outfit


def show_saved_outfits_page():
    st.title("Saved Outfits")

    user_id = st.session_state.get("user_id")
    if user_id is None:
        st.error("User not logged in.")
        return

    outfits = get_saved_outfits(user_id)

    if not outfits:
        st.info("No saved outfits yet.")
        return

    project_root = Path(__file__).resolve().parents[1]
    uploads_dir = project_root / "src" / "uploads"

    for outfit in outfits:
        with st.container():
            st.subheader(outfit.get("outfit_name") or "Unnamed Outfit")

            meta_cols = st.columns(3)
            with meta_cols[0]:
                st.write(f"**Season:** {outfit.get('season') or 'N/A'}")
            with meta_cols[1]:
                st.write(f"**Occasion:** {outfit.get('occasion') or 'N/A'}")
            with meta_cols[2]:
                st.write(f"**Outfit ID:** {outfit.get('id')}")

            items = outfit.get("items", [])

            if not items:
                st.warning("No items found in this outfit.")
            else:
                item_cols = st.columns(4)

                for i, item in enumerate(items):
                    col = item_cols[i % 4]

                    with col:
                        image_url = item.get("image_url")
                        if image_url:
                            filename = Path(image_url).name
                            real_image_path = uploads_dir / filename

                            if real_image_path.exists():
                                st.image(str(real_image_path), width=140)

                        st.caption(item.get("item_name") or "Unnamed Item")
                        st.write(f"Category: {item.get('category') or 'N/A'}")
                        st.write(f"Color: {item.get('color') or 'N/A'}")

            if st.button("Delete Outfit", key=f"delete_outfit_{outfit.get('id')}"):
                result = delete_outfit(outfit.get("id"))

                if result:
                    st.success("Outfit deleted successfully!")
                    st.rerun()
                else:
                    st.error("Failed to delete outfit.")

            st.divider()