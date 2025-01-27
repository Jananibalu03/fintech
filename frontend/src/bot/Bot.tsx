import { useState, useEffect, useRef } from "react";

interface ChatMessage {
    message: string;
    isCentered: boolean;
    sender?: "User" | "Bot";
}

export default function Bot() {

    const [userMessage, setUserMessage] = useState("");
    const [chat, setChat] = useState<ChatMessage[]>([
        { message: "Welcome! Ask me about stocks!", isCentered: true },
    ]);

    const [isChatOpen, setIsChatOpen] = useState(false);
    const chatWindowRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    }, [chat]);

    const handleSend = () => {

        const botResponses: Record<string, string> = {
            "What is a good stock to buy?": "I recommend looking into Apple (AAPL) or Microsoft (MSFT).",
            "Should I sell Tesla stock?": "It depends on your financial goals, but holding might be a good idea right now.",
            "What is the best stock for long-term investment?": "Consider Amazon (AMZN) for long-term growth.",
        };

        const response =
            botResponses[userMessage] || "I'm sorry, I don't have an answer for that. Try asking something else!";

        setChat((prevChat) => [
            ...prevChat,
            { message: userMessage, isCentered: false, sender: "User" },
            { message: response, isCentered: false, sender: "Bot" },
        ]);
        setUserMessage("");
    };

    return (
        <div>
            <div
                className={`chat-icon ${isChatOpen ? "chat-open" : ""}`}
                onClick={() => setIsChatOpen(!isChatOpen)}
            >
                💬
            </div>
            {isChatOpen && (
                <div className="chat-container">
                    <div className="bot-container">
                        <h1 className="bot-title">Stock Suggestion Bot</h1>
                        <div className="bot-chat-window" ref={chatWindowRef}>
                            {chat.map((entry, index) => (
                                <div
                                    key={index}
                                    className={`chat-bubble ${entry.isCentered
                                        ? "centered-bubble"
                                        : entry.sender === "User"
                                            ? "user-bubble"
                                            : "bot-bubble"
                                        }`}
                                >
                                    {entry.message}
                                </div>
                            ))}
                        </div>

                        <div className="bot-input-container">
                            <input
                                type="text"
                                value={userMessage}
                                onChange={(e) => setUserMessage(e.target.value)}
                                placeholder="Ask a question..."
                                className="bot-input"
                            />
                            <button onClick={handleSend} className="bot-send-button">
                                Send
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
