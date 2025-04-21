import { create } from 'zustand';
import axios from 'axios';

interface CandidateProfile {
  id: string;
  user: string;
  phone_number: string;
  location: string;
  current_position: string;
  years_of_experience: number;
  skills: string;
  education: string;
  resume: string;
  created_at: string;
  updated_at: string;
}

interface CandidateSkill {
  id: string;
  candidate: string;
  skill_name: string;
  skill_level: string;
  years_of_experience: number;
}

interface CandidateExperience {
  id: string;
  candidate: string;
  company_name: string;
  position: string;
  start_date: string;
  end_date: string | null;
  current_job: boolean;
  description: string;
}

interface CandidateState {
  profile: CandidateProfile | null;
  skills: CandidateSkill[];
  experiences: CandidateExperience[];
  isLoading: boolean;
  error: string | null;
  fetchProfile: () => Promise<void>;
  updateProfile: (profileData: Partial<CandidateProfile>) => Promise<void>;
  addSkill: (skillData: Omit<CandidateSkill, 'id' | 'candidate'>) => Promise<void>;
  removeSkill: (skillId: string) => Promise<void>;
  addExperience: (experienceData: Omit<CandidateExperience, 'id' | 'candidate'>) => Promise<void>;
  updateExperience: (id: string, experienceData: Partial<CandidateExperience>) => Promise<void>;
  removeExperience: (experienceId: string) => Promise<void>;
}

export const useCandidateStore = create<CandidateState>((set) => ({
  profile: null,
  skills: [],
  experiences: [],
  isLoading: false,
  error: null,
  fetchProfile: async () => {
    set({ isLoading: true, error: null });
    try {
      const [profileResponse, skillsResponse, experiencesResponse] = await Promise.all([
        axios.get('/api/candidates/profile/'),
        axios.get('/api/candidates/skills/'),
        axios.get('/api/candidates/experiences/'),
      ]);
      set({
        profile: profileResponse.data,
        skills: skillsResponse.data,
        experiences: experiencesResponse.data,
        isLoading: false,
      });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  updateProfile: async (profileData: Partial<CandidateProfile>) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.patch('/api/candidates/profile/', profileData);
      set({ profile: response.data, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  addSkill: async (skillData: Omit<CandidateSkill, 'id' | 'candidate'>) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.post('/api/candidates/skills/', skillData);
      set((state) => ({
        skills: [...state.skills, response.data],
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  removeSkill: async (skillId: string) => {
    set({ isLoading: true, error: null });
    try {
      await axios.delete(`/api/candidates/skills/${skillId}/`);
      set((state) => ({
        skills: state.skills.filter((skill) => skill.id !== skillId),
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  addExperience: async (experienceData: Omit<CandidateExperience, 'id' | 'candidate'>) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.post('/api/candidates/experiences/', experienceData);
      set((state) => ({
        experiences: [...state.experiences, response.data],
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  updateExperience: async (id: string, experienceData: Partial<CandidateExperience>) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.patch(`/api/candidates/experiences/${id}/`, experienceData);
      set((state) => ({
        experiences: state.experiences.map((exp) =>
          exp.id === id ? response.data : exp
        ),
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  removeExperience: async (experienceId: string) => {
    set({ isLoading: true, error: null });
    try {
      await axios.delete(`/api/candidates/experiences/${experienceId}/`);
      set((state) => ({
        experiences: state.experiences.filter((exp) => exp.id !== experienceId),
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
})); 