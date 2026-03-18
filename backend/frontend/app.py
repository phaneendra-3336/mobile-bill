import streamlit as st
import requests

st.title("📱 Postpaid Mobile Bill Calculator")

# Customer details
name = st.text_input("Customer Name")
mobile = st.text_input("Mobile Number")
city = st.text_input("City")

st.subheader("Usage Details")

minutes = st.number_input("Minutes Used", min_value=0)
texts = st.number_input("Text Messages Sent", min_value=0)

if st.button("Generate Bill"):

    # ✅ Validation
    if not name or not mobile or not city:
        st.warning("Please fill all details")
    else:
        payload = {
            "name": name,
            "mobile": mobile,
            "city": city,
            "minutes": int(minutes),
            "texts": int(texts)
        }

        try:
            response = requests.post(
                "https://mobile-bill-backend.onrender.com/generate_bill",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()

                st.subheader("Customer Bill")

                st.write("Name:", result["Customer Name"])
                st.write("Mobile:", result["Mobile Number"])
                st.write("City:", result["City"])
                st.write("Date:", result["Date"])

                st.markdown("---")

                st.write(f"Base Charge: ${result['Base Charge']:.2f}")

                if result["Extra Minutes Charge"] > 0:
                    st.write(f"Extra Minutes Charge: ${result['Extra Minutes Charge']:.2f}")

                if result["Extra Text Charge"] > 0:
                    st.write(f"Extra Text Charge: ${result['Extra Text Charge']:.2f}")

                st.write(f"Call Center Price: ${result['Call Center Price']:.2f}")
                st.write(f"Tax: ${result['Tax']:.2f}")

                st.markdown("### Total Bill")
                st.success(f"${result['Total Bill']:.2f}")

            else:
                st.error(f"Server Error: {response.status_code}")
                st.text(response.text)

        except Exception as e:
            st.error(f"Backend not reachable: {e}")