"use client"

import { useEffect, useState } from 'react';
import { spotify } from '@/services/spotify';

interface Track {
  id: string;
  name: string;
  artists: { name: string }[];
  album: {
    name: string;
    images: { url: string }[];
  };
}

export default function Dashboard() {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [timeRange, setTimeRange] = useState('medium_term');

  useEffect(() => {
    const fetchTracks = async () => {
      try {
        const data = await spotify.getTopTracks(timeRange);
        setTracks(data.items);
      } catch (error) {
        console.error('Failed to fetch tracks:', error);
      }
    };

    fetchTracks();
  }, [timeRange]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-black to-gray-900 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-8">Your Top Tracks</h1>
        
        <div className="flex gap-4 mb-8">
          <button
            onClick={() => setTimeRange('short_term')}
            className={`px-4 py-2 rounded-full ${
              timeRange === 'short_term' 
                ? 'bg-green-500 text-white' 
                : 'bg-gray-800 text-gray-300'
            }`}
          >
            Last Month
          </button>
          <button
            onClick={() => setTimeRange('medium_term')}
            className={`px-4 py-2 rounded-full ${
              timeRange === 'medium_term' 
                ? 'bg-green-500 text-white' 
                : 'bg-gray-800 text-gray-300'
            }`}
          >
            Last 6 Months
          </button>
          <button
            onClick={() => setTimeRange('long_term')}
            className={`px-4 py-2 rounded-full ${
              timeRange === 'long_term' 
                ? 'bg-green-500 text-white' 
                : 'bg-gray-800 text-gray-300'
            }`}
          >
            All Time
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tracks.map((track) => (
            <div
              key={track.id}
              className="bg-gray-800 rounded-lg overflow-hidden hover:bg-gray-700 transition-colors"
            >
              <img
                src={track.album.images[0]?.url}
                alt={track.album.name}
                className="w-full aspect-square object-cover"
              />
              <div className="p-4">
                <h3 className="text-white font-semibold">{track.name}</h3>
                <p className="text-gray-400">
                  {track.artists.map(a => a.name).join(', ')}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
