import React, { useState, useRef, useEffect } from 'react';
import { Box, TextField, IconButton, Paper, Typography, Avatar, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import { ChatMessage, DiagnosisResponse } from '../types';
import DiagnosisCard from './DiagnosisCard';

const Chat: React.FC = () => {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage: ChatMessage = {
            id: Date.now().toString(),
            text: input,
            sender: 'user',
            timestamp: new Date(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await axios.post<DiagnosisResponse>('http://localhost:8000/diagnose', {
                text: input,
            });

            // Get Wikipedia image
            const wikiResponse = await axios.get(
                `https://en.wikipedia.org/w/api.php?action=query&titles=${encodeURIComponent(
                    response.data.disease_info.disease
                )}&prop=pageimages&format=json&pithumbsize=300&origin=*`
            );

            const pages = wikiResponse.data.query.pages;
            const pageId = Object.keys(pages)[0];
            const imageUrl = pages[pageId]?.thumbnail?.source;

            const botMessage: ChatMessage = {
                id: (Date.now() + 1).toString(),
                text: 'Here\'s what I found:',
                sender: 'bot',
                timestamp: new Date(),
                diagnosis: {
                    ...response.data,
                    wikipedia_image: imageUrl,
                },
            };

            setMessages((prev) => [...prev, botMessage]);
        } catch (error) {
            console.error('Error:', error);
            const errorMessage: ChatMessage = {
                id: (Date.now() + 1).toString(),
                text: 'Sorry, I encountered an error. Please try again.',
                sender: 'bot',
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box
            sx={{
                height: '100vh',
                display: 'flex',
                flexDirection: 'column',
                bgcolor: '#f5f5f5',
            }}
        >
            <Box
                sx={{
                    flex: 1,
                    overflow: 'auto',
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    gap: 2,
                }}
            >
                <AnimatePresence>
                    {messages.map((message) => (
                        <motion.div
                            key={message.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            transition={{ duration: 0.3 }}
                        >
                            <Box
                                sx={{
                                    display: 'flex',
                                    justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                                    gap: 1,
                                }}
                            >
                                {message.sender === 'bot' && (
                                    <Avatar sx={{ bgcolor: 'primary.main' }}>MD</Avatar>
                                )}
                                <Paper
                                    sx={{
                                        p: 2,
                                        maxWidth: '70%',
                                        bgcolor: message.sender === 'user' ? 'primary.main' : 'white',
                                        color: message.sender === 'user' ? 'white' : 'text.primary',
                                    }}
                                >
                                    <Typography>{message.text}</Typography>
                                    {message.diagnosis && <DiagnosisCard diagnosis={message.diagnosis} />}
                                </Paper>
                                {message.sender === 'user' && (
                                    <Avatar sx={{ bgcolor: 'secondary.main' }}>U</Avatar>
                                )}
                            </Box>
                        </motion.div>
                    ))}
                </AnimatePresence>
                <div ref={messagesEndRef} />
            </Box>
            <Box
                sx={{
                    p: 2,
                    bgcolor: 'background.paper',
                    borderTop: 1,
                    borderColor: 'divider',
                }}
            >
                <Box sx={{ display: 'flex', gap: 1 }}>
                    <TextField
                        fullWidth
                        variant="outlined"
                        placeholder="Describe your symptoms..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                        disabled={loading}
                    />
                    <IconButton
                        color="primary"
                        onClick={handleSend}
                        disabled={loading || !input.trim()}
                    >
                        {loading ? <CircularProgress size={24} /> : <SendIcon />}
                    </IconButton>
                </Box>
            </Box>
        </Box>
    );
};

export default Chat; 