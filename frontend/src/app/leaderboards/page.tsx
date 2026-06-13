'use client';

import { useEffect, useState } from 'react';
import { api } from '@/utils/api';
import { motion } from 'framer-motion';
import { Crown, Loader2 } from 'lucide-react';
import { format } from 'date-fns';

interface LeaderboardEntry {
  rank: number;
  user: {
    username: string;
    profile: {
      level: number;
    }
  };
  wpm: number;
  accuracy: number;
  raw_wpm: number;
  consistency: number;
  date: string;
}

export default function LeaderboardsPage() {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const response = await api.get('/leaderboards/global/');
        if (response.data.success) {
          setEntries(response.data.data.entries || []);
        }
      } catch (error) {
        console.error('Failed to fetch leaderboards:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchLeaderboard();
  }, []);

  return (
    <div className="w-full max-w-5xl mx-auto flex flex-col font-mono text-[var(--sub-color)] mt-8">
      <div className="flex items-center gap-3 mb-8 text-[var(--text-color)]">
        <Crown className="w-8 h-8 text-[var(--main-color)]" />
        <div>
          <h1 className="text-2xl font-bold">All-time Global Leaderboard</h1>
          <p className="text-sm text-[var(--sub-color)]">Top typists across all time modes</p>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center py-24">
          <Loader2 className="w-8 h-8 animate-spin text-[var(--main-color)]" />
        </div>
      ) : (
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full overflow-x-auto"
        >
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-[var(--sub-color)]/20 text-xs text-[var(--sub-color)]">
                <th className="py-4 px-4 font-normal">#</th>
                <th className="py-4 px-4 font-normal">name</th>
                <th className="py-4 px-4 font-normal">wpm</th>
                <th className="py-4 px-4 font-normal">accuracy</th>
                <th className="py-4 px-4 font-normal">raw</th>
                <th className="py-4 px-4 font-normal">consistency</th>
                <th className="py-4 px-4 font-normal text-right">date</th>
              </tr>
            </thead>
            <tbody>
              {entries.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-[var(--sub-color)]/70">
                    no entries found
                  </td>
                </tr>
              ) : (
                entries.map((entry, index) => (
                  <tr 
                    key={index}
                    className="border-b border-[var(--sub-color)]/10 hover:bg-[var(--sub-color)]/5 transition-colors group"
                  >
                    <td className="py-4 px-4 text-[var(--text-color)] font-bold">{entry.rank}</td>
                    <td className="py-4 px-4 text-[var(--main-color)] flex items-center gap-2">
                      {entry.user.username}
                      <span className="text-[10px] bg-[var(--sub-color)]/10 text-[var(--sub-color)] px-1.5 py-0.5 rounded">
                        lvl {entry.user.profile?.level || 1}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-[var(--text-color)] font-bold">{Math.round(entry.wpm)}</td>
                    <td className="py-4 px-4">{entry.accuracy.toFixed(2)}%</td>
                    <td className="py-4 px-4">{Math.round(entry.raw_wpm)}</td>
                    <td className="py-4 px-4">{entry.consistency.toFixed(2)}%</td>
                    <td className="py-4 px-4 text-right text-xs">
                      {format(new Date(entry.date), 'dd MMM yyyy')}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </motion.div>
      )}
    </div>
  );
}
