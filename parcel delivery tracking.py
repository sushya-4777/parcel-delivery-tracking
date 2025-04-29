import streamlit as st
import hashlib
import time
import json

# --- Block and Blockchain Classes ---
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{json.dumps(self.data)}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), {"location": "Warehouse", "status": "Order Placed"}, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_data):
        prev_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), new_data, prev_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# --- Streamlit App ---

# Store blockchain in session
if "parcel_chain" not in st.session_state:
    st.session_state.parcel_chain = Blockchain()

st.title("📦 Parcel Delivery Tracking Blockchain")

# --- Form to Add a Block ---
st.header("➕ Add Delivery Update")
with st.form("add_block_form"):
    location = st.text_input("Location")
    status = st.text_input("Status")
    submitted = st.form_submit_button("Add Block")
    if submitted:
        if location and status:
            st.session_state.parcel_chain.add_block({"location": location, "status": status})
            st.success("✅ Block added to the blockchain.")
        else:
            st.warning("Please enter both location and status.")

# --- Display Blockchain ---
st.header("📜 Blockchain Ledger (Full View)")
for block in st.session_state.parcel_chain.chain:
    st.markdown(f"### 🧱 Block #{block.index}")
    st.write(f"**Timestamp:** {time.ctime(block.timestamp)}")
    st.write("**Data:**")
    st.json(block.data)
    st.write(f"**Hash:** `{block.hash}`")
    st.write(f"**Previous Hash:** `{block.previous_hash}`")
    st.markdown("---")

# --- Validate Blockchain ---
st.header("✅ Blockchain Validity Check")
if st.session_state.parcel_chain.is_chain_valid():
    st.success("The blockchain is valid.")
else:
    st.error("⚠️ Blockchain integrity has been compromised.")
