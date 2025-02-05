import { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { BotData } from "./BotSlice";

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

    const dispatch = useDispatch();
    const { loading, BotDataSuccess, BotDataPayload } = useSelector(
        (state: any) => state.Bot
    );

    useEffect(() => {
        if (BotDataSuccess && BotDataPayload) {
            setChat((prevChat) => [
                ...prevChat,
                { message: BotDataPayload, isCentered: false, sender: "Bot" },
            ]);
        }
    }, [BotDataPayload]);

    useEffect(() => {
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    }, [chat]);

    const handleSend = () => {
        if (!userMessage.trim()) return;

        setChat((prevChat) => [
            ...prevChat,
            { message: userMessage, isCentered: false, sender: "User" },
        ]);

        dispatch<any>(BotData(userMessage));
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
                        <div
                            className="bot-chat-window"
                            ref={chatWindowRef}

                        >

                            {chat.map((entry, index) => (
                                <div
                                    key={index}
                                    className={`chat-bubble ${entry.isCentered
                                        ? "centered-bubble"
                                        : entry.sender === "User"
                                            ? "user-bubble"
                                            : "bot-bubble"
                                        }`}
                                    dangerouslySetInnerHTML={{ __html: entry.message }}
                                />
                            ))}
                            {loading && <div className="chat-bubble">Loading...</div>}
                        </div>

                        <div className="bot-input-container">
                            <input
                                type="text"
                                value={userMessage}
                                onChange={(e) => setUserMessage(e.target.value)}
                                onKeyDown={(e) => {
                                    if (e.key === "Enter") {
                                        handleSend();
                                    }
                                }}
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
