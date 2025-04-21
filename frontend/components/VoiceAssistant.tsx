import { useState, useEffect } from 'react';
import { MicrophoneIcon, StopIcon } from '@heroicons/react/24/solid';
import { useVapi } from '@/hooks/useVapi';
import { useJobStore } from '@/store/jobStore';
import { useCandidateStore } from '@/store/candidateStore';
import { useInterviewStore } from '@/store/interviewStore';

export const VoiceAssistant = () => {
  const [isListening, setIsListening] = useState(false);
  const [command, setCommand] = useState('');
  const { startListening, stopListening, transcript } = useVapi();
  const { fetchJobs, createJob } = useJobStore();
  const { fetchProfile, updateProfile } = useCandidateStore();
  const { scheduleInterview } = useInterviewStore();

  useEffect(() => {
    if (transcript) {
      setCommand(transcript);
      handleVoiceCommand(transcript);
    }
  }, [transcript]);

  const handleVoiceToggle = async () => {
    if (isListening) {
      await stopListening();
    } else {
      await startListening();
    }
    setIsListening(!isListening);
  };

  const handleVoiceCommand = async (command: string) => {
    const lowerCommand = command.toLowerCase();

    if (lowerCommand.includes('post job')) {
      // Extract job details from command
      const title = extractValue(command, 'title');
      const description = extractValue(command, 'description');
      const requirements = extractValue(command, 'requirements');
      const location = extractValue(command, 'location');
      const salary = extractValue(command, 'salary');

      if (title && description && requirements && location && salary) {
        await createJob({
          title,
          description,
          requirements,
          location,
          salary_range: salary,
          job_type: 'Full-time',
          experience_level: 'Mid-level',
        });
      }
    } else if (lowerCommand.includes('update profile')) {
      const phone = extractValue(command, 'phone');
      const location = extractValue(command, 'location');
      const position = extractValue(command, 'position');

      if (phone || location || position) {
        await updateProfile({
          phone_number: phone,
          location,
          current_position: position,
        });
      }
    } else if (lowerCommand.includes('schedule interview')) {
      const candidate = extractValue(command, 'candidate');
      const date = extractValue(command, 'date');
      const time = extractValue(command, 'time');

      if (candidate && date && time) {
        await scheduleInterview({
          candidate,
          scheduled_date: `${date}T${time}`,
          duration: 60,
          status: 'SCHEDULED',
        });
      }
    } else if (lowerCommand.includes('search jobs')) {
      await fetchJobs();
    } else if (lowerCommand.includes('view profile')) {
      await fetchProfile();
    }
  };

  const extractValue = (command: string, key: string): string => {
    const regex = new RegExp(`${key}\\s*[:=]\\s*([^\\s]+)`, 'i');
    const match = command.match(regex);
    return match ? match[1] : '';
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <div className="flex flex-col items-center space-y-2">
        <button
          onClick={handleVoiceToggle}
          className={`p-4 rounded-full ${
            isListening ? 'bg-red-500' : 'bg-primary-500'
          } text-white transition-colors shadow-lg hover:shadow-xl`}
        >
          {isListening ? (
            <StopIcon className="h-8 w-8" />
          ) : (
            <MicrophoneIcon className="h-8 w-8" />
          )}
        </button>
        {isListening && (
          <div className="bg-white rounded-lg p-4 shadow-lg max-w-md">
            <p className="text-sm text-gray-600">Listening...</p>
            {command && (
              <p className="mt-2 text-gray-800 font-medium">{command}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}; 