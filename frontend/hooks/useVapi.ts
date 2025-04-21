import { useState, useEffect } from 'react';
import { createClient } from '@vapi-ai/web';

interface VapiConfig {
  apiKey: string;
  assistantId: string;
}

export const useVapi = () => {
  const [transcript, setTranscript] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [vapiClient, setVapiClient] = useState<any>(null);

  useEffect(() => {
    const config: VapiConfig = {
      apiKey: process.env.NEXT_PUBLIC_VAPI_API_KEY || '',
      assistantId: process.env.NEXT_PUBLIC_VAPI_ASSISTANT_ID || '',
    };

    const client = createClient(config);
    setVapiClient(client);

    return () => {
      if (client) {
        client.destroy();
      }
    };
  }, []);

  const startListening = async () => {
    if (!vapiClient) return;

    try {
      await vapiClient.start();
      setIsListening(true);

      vapiClient.on('transcript', (data: { text: string }) => {
        setTranscript(data.text);
      });

      vapiClient.on('error', (error: Error) => {
        console.error('Vapi error:', error);
        setIsListening(false);
      });
    } catch (error) {
      console.error('Error starting Vapi:', error);
      setIsListening(false);
    }
  };

  const stopListening = async () => {
    if (!vapiClient) return;

    try {
      await vapiClient.stop();
      setIsListening(false);
      setTranscript('');
    } catch (error) {
      console.error('Error stopping Vapi:', error);
    }
  };

  return {
    transcript,
    isListening,
    startListening,
    stopListening,
  };
}; 