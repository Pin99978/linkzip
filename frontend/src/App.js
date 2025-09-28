import React from 'react';
import './App.css';
import ShortenerForm from './components/ShortenerForm';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>LinkZip</h1>
                <p>The one-stop solution for your URL shortening needs.</p>
            </header>
            <main className="main-content">
                <ShortenerForm 
                    title="🔗 Shorten a Web Page"
                    placeholder="Enter a long URL here"
                />
                <ShortenerForm 
                    title="🖼️ Shorten an Image URL"
                    placeholder="Enter an image URL here"
                />
                <ShortenerForm 
                    title="🎬 Shorten a Video URL"
                    placeholder="Enter a video URL here"
                />
            </main>
        </div>
    );
}

export default App;