import React, { useState } from "react";
import { FiMic, FiMicOff } from "react-icons/fi";

/*
 * Voice assistant built on the browser's native Web Speech API
 * (SpeechRecognition + SpeechSynthesis) -- works fully offline of any
 * paid service, in Chrome/Edge. Supports English and Marathi.
 * Extend the intents map below to wire up more commands
 * (e.g. sendPrompt-style navigation, reading out prediction results).
 */
const LANG_MAP = { en: "en-IN", mr: "mr-IN" };

const RESPONSES = {
  en: {
    greeting: "Hello farmer! How can I help you today?",
    unknown: "Sorry, I did not understand that. Try saying 'upload image', 'crop recommendation', 'risk prediction', 'farm profile', 'market prices', or 'show weather'.",
    upload: "Opening the disease detection page for you.",
    weather: "Opening weather risk page for you.",
    history: "Opening your crop history.",
    crop: "Opening crop recommendation page for you.",
    risk: "Opening risk prediction page for you.",
    farm: "Opening your farm profile.",
    market: "Opening market prices for you.",
    reports: "Opening your reports page.",
  },
  mr: {
    greeting: "नमस्कार शेतकरी! मी आपली कशी मदत करू शकतो?",
    unknown: "माफ करा, मला ते समजले नाही. 'फोटो अपलोड करा', 'पीक शिफारस', 'धोका अंदाज', 'शेत प्रोफाइल', 'बाजार भाव' किंवा 'हवामान दाखवा' असे बोलून पहा.",
    upload: "रोग तपासणी पान उघडत आहे.",
    weather: "हवामान जोखीम पान उघडत आहे.",
    history: "आपला पीक इतिहास उघडत आहे.",
    crop: "पीक शिफारस पान उघडत आहे.",
    risk: "धोका अंदाज पान उघडत आहे.",
    farm: "आपले शेत प्रोफाइल उघडत आहे.",
    market: "बाजार भाव उघडत आहे.",
    reports: "अहवाल पान उघडत आहे.",
  },
};

export default function VoiceAssistant() {
  const [lang, setLang] = useState("en");
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const supported = typeof window !== "undefined" &&
    (window.SpeechRecognition || window.webkitSpeechRecognition);

  const speak = (text) => {
    if (!window.speechSynthesis) return;
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = LANG_MAP[lang];
    window.speechSynthesis.speak(utter);
  };

  const handleCommand = (text) => {
    const lower = text.toLowerCase();
    const r = RESPONSES[lang];

    const routes = [
      { keys: ["crop recommendation", "पीक शिफारस", "पीक सुचव"], path: "/crop-recommendation", say: r.crop },
      { keys: ["risk prediction", "risk", "धोका", "जोखीम"], path: "/risk-prediction", say: r.risk },
      { keys: ["farm profile", "farm", "शेत प्रोफाइल", "शेत माहिती"], path: "/farm-profile", say: r.farm },
      { keys: ["market", "price", "बाजार", "भाव"], path: "/market", say: r.market },
      { keys: ["report", "अहवाल"], path: "/reports", say: r.reports },
      { keys: ["weather", "हवामान"], path: "/weather", say: r.weather },
      { keys: ["history", "इतिहास"], path: "/history", say: r.history },
      { keys: ["upload", "फोटो", "detect"], path: "/upload", say: r.upload },
    ];

    const match = routes.find((route) => route.keys.some((k) => lower.includes(k)));
    if (match) {
      speak(match.say);
      window.location.href = match.path;
    } else {
      speak(r.unknown);
    }
  };

  const startListening = () => {
    if (!supported) {
      speak(RESPONSES[lang].unknown);
      return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = LANG_MAP[lang];
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    setListening(true);
    speak(RESPONSES[lang].greeting);

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      setTranscript(text);
      handleCommand(text);
    };
    recognition.onerror = () => setListening(false);
    recognition.onend = () => setListening(false);
    recognition.start();
  };

  return (
    <div className="voice-assistant">
      <select
        value={lang}
        onChange={(e) => setLang(e.target.value)}
        className="voice-lang-select"
        title="Voice assistant language"
      >
        <option value="en">EN</option>
        <option value="mr">मराठी</option>
      </select>
      <button
        className={`icon-toggle ${listening ? "listening" : ""}`}
        onClick={startListening}
        title="Voice assistant"
      >
        {listening ? <FiMicOff /> : <FiMic />}
      </button>
      {transcript && <span className="voice-transcript">"{transcript}"</span>}
    </div>
  );
}
