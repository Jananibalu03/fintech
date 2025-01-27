import whitelogo from "../../assets/images/whitelogo.png";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTwitter, faLinkedin, faInstagram, faFacebook } from '@fortawesome/free-brands-svg-icons';
import { faEnvelope, faPhone, faLocationDot } from '@fortawesome/free-solid-svg-icons';


export default function Footer() {

    return (
        <footer>
            <div className="footer-container">
                <div className="footer-section">
                    <img src={whitelogo} alt='logo' />
                    <p>Your trusted platform for stock recommendations, analysis,<br /> and financial insights.</p>
                </div>

                <div className="footer-section">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="/about">About Us</a></li>
                        <li><a href="/services">Services</a></li>
                        <li><a href="/blog">Blog</a></li>
                        <li><a href="/contact">Contact</a></li>
                    </ul>
                </div>

                <div className="footer-section">
                    <h3>Contact Us</h3>
                    <p><FontAwesomeIcon icon={faEnvelope} className="me-2" />
                        support@gmail.com</p>
                    <p><FontAwesomeIcon icon={faPhone} className="me-2" /> +1 800-555-1234</p>
                    <p><FontAwesomeIcon icon={faLocationDot} className="me-2" /> 123 Finance Street, New York, NY</p>
                </div>

                <div className="footer-section">
                    <h3>Follow Us</h3>
                    <div className="social-icons">
                        <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">
                            <FontAwesomeIcon icon={faFacebook} />
                        </a>
                        <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">
                            <FontAwesomeIcon icon={faTwitter} />
                        </a>
                        <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer">
                            <FontAwesomeIcon icon={faLinkedin} />
                        </a>
                        <a href="https://instagram.com" target="_blank" rel="noopener noreferrer">
                            <FontAwesomeIcon icon={faInstagram} />
                        </a>
                    </div>
                </div>
            </div>

            <div className="copyright">
                © {new Date().getFullYear()} Adhiran Infotech. All Rights Reserved.
            </div>
        </footer>
    );
}
