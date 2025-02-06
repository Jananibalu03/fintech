import { useState, useEffect } from 'react';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { useLocation, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { forgetpassword, resetpassword } from "./LoginSlice";
import { RootState } from '../store/Store';

const PasswordSchema = Yup.object().shape({
  password: Yup.string().required('Password Required'),
  confirm_password: Yup.string()
    .oneOf([Yup.ref('password')], 'Passwords must match')
    .required('Confirm Password Required'),
});

const emailSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email').required('Email Required'),
});

export default function ForgotPassword() {
  const location = useLocation();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { error, resetpasswordPayload, forgetpasswordPayload } = useSelector((state: RootState) => state.login);

  console.log("1", resetpasswordPayload?.message);
  console.log("2", forgetpasswordPayload?.message);

  
  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [token, setToken] = useState(null);

  useEffect(() => {
    const urlParams = new URLSearchParams(location.search);
    const tokenFromUrl = urlParams.get("token");

    if (location.pathname === "/resetpassword") {
      if (!tokenFromUrl) {
        navigate("/");
      } else {
        setToken(tokenFromUrl);
        setShowPasswordForm(true);
      }
    }
  }, [location, navigate]);

  const handleEmailSubmit = async (values:any) => {
    setIsSubmitting(true);
    dispatch<any>(forgetpassword(values))
      .unwrap()
      .then(() => {
        setShowModal(true);
      })
      .catch(() => {
        setShowModal(true);
      })
      .finally(() => {
        setIsSubmitting(false);
      });
  };


  const handlePasswordSubmit = async (values: { password: string; confirm_password: string }) => {
    setIsSubmitting(true);
    try {
      const token = new URLSearchParams(window.location.search).get("token");
      if (!token) {
        throw new Error("Token is missing in URL");
      }
      await dispatch<any>(resetpassword({
        token,
        password: values.password,
        confirm_password: values.confirm_password
      })).unwrap();

      setShowModal(true);

    } catch (error) {
      console.error("Reset Password Error:", error);
    }
    setIsSubmitting(false);
  };


  const handleCloses = () => {
    setShowModal(false);
    navigate('/')
  };

  return (
    <div className="container d-flex vh-100 align-items-center justify-content-center">
      <div className="row w-100 justify-content-center">
        <div className="col-12 col-md-6 col-lg-4">
          <div className="card shadow p-4">
            <h4 className="text-center mb-4">{showPasswordForm ? "Reset Password" : "Forgot Password"}</h4>
            {!showPasswordForm ? (
              <Formik
                initialValues={{ email: '' }}
                validationSchema={emailSchema}
                onSubmit={handleEmailSubmit}
              >
                {({ errors, touched }) => (
                  <Form>
                    <label className="form-label">Enter your email to reset password</label>
                    <Field name="email" type="email" placeholder="Enter your email" className="form-control" />
                    {errors.email && touched.email && <div className="text-danger">{errors.email}</div>}
                    <div className="text-center mt-4">
                      <button type="submit" className="common-btn p-2 w-100" disabled={isSubmitting}>
                        {isSubmitting ? "Sending..." : "Send Reset Link"}
                      </button>
                    </div>
                  </Form>
                )}
              </Formik>
            ) : (
              <Formik
                initialValues={{ password: '', confirm_password: '' }}
                validationSchema={PasswordSchema}
                onSubmit={handlePasswordSubmit}
              >
                {({ errors, touched }) => (
                  <Form>
                    <label className="form-label">New Password</label>
                    <Field name="password" type="password" placeholder="Enter new password" className="form-control" />
                    {errors.password && touched.password && <div className="text-danger">{errors.password}</div>}
                    <label className="form-label pt-3">Confirm Password</label>
                    <Field name="confirm_password" type="password" placeholder="Confirm new password" className="form-control" />
                    {errors.confirm_password && touched.confirm_password && <div className="text-danger">{errors.confirm_password}</div>}
                    <div className="text-center mt-4">
                      <button type="submit" className="common-btn p-2 w-100" disabled={isSubmitting}>
                        {isSubmitting ? "Saving..." : "Submit"}
                      </button>
                    </div>
                  </Form>
                )}
              </Formik>
            )}
          </div>
        </div>
      </div>

      {showModal && (
        <div className="modal fade show d-block" tabIndex={-1} style={{ background: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-body text-center">
                <p>{error || forgetpasswordPayload?.message || resetpasswordPayload?.message}</p>
              </div>
              <div className="text-center py-3 pt-0">
                <button type="button" className="common-btn p-2" onClick={handleCloses}>
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
