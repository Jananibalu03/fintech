import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { registration } from "./LoginSlice";
import { RootState } from "../store/Store";

export default function Registration() {

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { loading, error } = useSelector(
    (state: RootState) => state.TopTrend
  );

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    dispatch<any>(registration(formData))
      .then((result) => {
        if (result.meta.requestStatus === "fulfilled") {
          navigate("/");
        }
      });
  };

  return (
    <div className="container d-flex justify-content-center align-items-center vh-100">
      <div className="card p-4 shadow-lg" style={{ width: "100%", maxWidth: "400px" }}>
        <h3 className="text-center mb-3">Register</h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Username</label>
            <input
              type="text"
              name="username"
              className="form-control"
              placeholder="Enter your username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Email</label>
            <input
              type="email"
              name="email"
              className="form-control"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Password</label>
            <input
              type="password"
              name="password"
              className="form-control"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Confirm Password</label>
            <input
              type="password"
              name="confirm_password"
              className="form-control"
              placeholder="Enter your password again"
              value={formData.confirm_password}
              onChange={handleChange}
              required
            />
          </div>

          {error && <div className="text-danger">{error}</div>}
          <button type="submit" className="common-btn p-2 w-100" disabled={loading}>
            {loading ? "Register in..." : "Register"}
          </button>
        </form>
        <p className="text-center mt-3">
          Already have an account? <a href="/">Login</a>
        </p>
      </div>
    </div>
  );
}
