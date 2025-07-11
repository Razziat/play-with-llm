import React from 'react';
import ChatBox from './ChatBox';

export default function App() {
  return (
    <div className="app-container" style={{ padding: '1rem', fontFamily: 'sans-serif' }}>
      <h1>Chatbot IA avec ou sans recherche web</h1>
      <ChatBox />
    </div>
  );
}
