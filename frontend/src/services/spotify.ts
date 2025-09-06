import { redirect } from 'next/navigation';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const spotify = {
    login: () => {
        window.location.href = `${BASE_URL}/spotify/login/`;
    },
    
    getUser: async () => {
        const response = await fetch(`${BASE_URL}/spotify/user/`, {
            credentials: 'include',
        });
        if (!response.ok) throw new Error('Failed to fetch user');
        return response.json();
    },

    getTopTracks: async (timeRange = 'medium_term') => {
        const response = await fetch(`${BASE_URL}/spotify/top-tracks/${timeRange}/`, {
            credentials: 'include',
        });
        if (!response.ok) throw new Error('Failed to fetch top tracks');
        return response.json();
    }
};
