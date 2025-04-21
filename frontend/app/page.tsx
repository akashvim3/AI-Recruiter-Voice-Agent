'use client';

import { useState } from 'react';
import { MicrophoneIcon, StopIcon } from '@heroicons/react/24/solid';
import { useVapi } from '@/hooks/useVapi';

export default function Home() {
  const [isListening, setIsListening] = useState(false);
  const { startListening, stopListening, transcript } = useVapi();

  const handleVoiceToggle = async () => {
    if (isListening) {
      await stopListening();
    } else {
      await startListening();
    }
    setIsListening(!isListening);
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI Recruiter Voice Agent
          </h1>
          <p className="text-xl text-gray-600">
            Streamline your hiring process with AI-powered voice technology
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="card">
            <h2 className="text-2xl font-semibold mb-4">Voice Interface</h2>
            <div className="flex flex-col items-center space-y-4">
              <button
                onClick={handleVoiceToggle}
                className={`p-4 rounded-full ${
                  isListening ? 'bg-red-500' : 'bg-primary-500'
                } text-white transition-colors`}
              >
                {isListening ? (
                  <StopIcon className="h-8 w-8" />
                ) : (
                  <MicrophoneIcon className="h-8 w-8" />
                )}
              </button>
              <p className="text-sm text-gray-500">
                {isListening ? 'Listening...' : 'Click to start voice interaction'}
              </p>
            </div>
            {transcript && (
              <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                <p className="text-gray-700">{transcript}</p>
              </div>
            )}
          </div>

          <div className="card">
            <h2 className="text-2xl font-semibold mb-4">Quick Actions</h2>
            <div className="grid grid-cols-2 gap-4">
              <button className="btn-primary">Post Job</button>
              <button className="btn-primary">View Candidates</button>
              <button className="btn-primary">Schedule Interview</button>
              <button className="btn-primary">Analytics</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
} 