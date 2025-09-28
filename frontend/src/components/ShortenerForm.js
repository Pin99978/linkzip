import React, { useState } from 'react';

const CopyIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
    </svg>
);

const CheckIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
);

function ShortenerForm({ title, placeholder }) {
    const [originalUrl, setOriginalUrl] = useState('');
    const [shortUrl, setShortUrl] = useState('');
    const [error, setError] = useState('');
    const [isCopied, setIsCopied] = useState(false);

    const handleCopy = async () => {
        if (!shortUrl) return;
        try {
            await navigator.clipboard.writeText(shortUrl);
            setIsCopied(true);
            setTimeout(() => {
                setIsCopied(false);
            }, 2000);
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setShortUrl('');
        setIsCopied(false);

        if (!originalUrl) {
            setError('Please enter a URL.');
            return;
        }

        try {
            const response = await fetch('/api/urls', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ original_url: originalUrl }),
            });

            const data = await response.json();

            if (!response.ok) {
                setError(data.detail || 'An error occurred.');
            } else {
                const fullShortUrl = `http://localhost:8000/${data.short_key}`;
                setShortUrl(fullShortUrl);
            }
        } catch (err) {
            setError('Failed to connect to the server.');
        }
    };

    return (
        <div className="shortener-card">
            <h3>{title}</h3>
            <form onSubmit={handleSubmit} className="url-form">
                <input
                    type="url"
                    value={originalUrl}
                    onChange={(e) => setOriginalUrl(e.target.value)}
                    placeholder={placeholder}
                    required
                />
                <button type="submit">Shorten</button>
            </form>
            {shortUrl && (
                <div className="result">
                    <a href={shortUrl} target="_blank" rel="noopener noreferrer">
                        {shortUrl}
                    </a>
                    <button onClick={handleCopy} className={`copy-button ${isCopied ? 'copied' : ''}`}>
                        {isCopied ? <CheckIcon /> : <CopyIcon />}
                    </button>
                </div>
            )}
            {error && (
                <div className="error">
                    <p>{error}</p>
                </div>
            )}
        </div>
    );
}

export default ShortenerForm;
