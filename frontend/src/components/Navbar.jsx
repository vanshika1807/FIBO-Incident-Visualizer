import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <div style={{
      padding: "15px",
      background: "#20232a",
      color: "white",
      display: "flex",
      gap: "20px"
    }}>
      <Link to="/" style={{ color: "white", textDecoration: "none" }}>Dashboard</Link>
      <Link to="/generate" style={{ color: "white", textDecoration: "none" }}>Generate</Link>
    </div>
  );
}
