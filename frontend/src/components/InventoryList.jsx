import React, { useState, useEffect } from "react";
import axios from "axios";

function InventoryList() {
  const [items, setItems] = useState([]);
  const [search, setSearch] = useState("");
  const [qrCode, setQrCode] = useState(null);

  useEffect(() => {
    fetchItems();
  }, [search]);

  const fetchItems = async () => {
    try {
      const response = await axios.get(`/api/items/?search=${search}`);
      setItems(response.data);
    } catch (error) {
      console.error("Error fetching items:", error);
    }
  };

  const fetchQrCode = async (itemId) => {
    try {
      const response = await axios.get(`/api/items/${itemId}/generate_qr/`);
      setQrCode(response.data.qr_code);
    } catch (error) {
      console.error("Error fetching QR code:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Inventory List</h2>
      <input
        type="text"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Search items..."
        style={{ marginBottom: "10px", padding: "5px", width: "200px" }}
      />
      <ul>
        {items.map((item) => (
          <li key={item.id} style={{ margin: "10px 0" }}>
            {item.name} - Quantity: {item.quantity}
            <button
              onClick={() => fetchQrCode(item.id)}
              style={{ marginLeft: "10px", padding: "5px" }}
            >
              Get QR Code
            </button>
          </li>
        ))}
      </ul>
      {qrCode && (
        <div>
          <h3>QR Code</h3>
          <img src={qrCode} alt="QR Code" style={{ maxWidth: "200px" }} />
        </div>
      )}
    </div>
  );
}

export default InventoryList;
