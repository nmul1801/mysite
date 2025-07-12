import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import { leagueApi } from '../services/api';
import type { LeagueAssemblyRequest, LeagueAssemblyResponse, ProgressUpdate } from '../services/types';

export const useLeagueAssembly = () => {
  const [progress, setProgress] = useState<ProgressUpdate | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);

  const assemblyMutation = useMutation({
    mutationFn: leagueApi.assembleScoring,
    onSuccess: (data) => {
      console.log('League assembled successfully:', data);
    },
    onError: (error) => {
      console.error('League assembly failed:', error);
    },
  });

  const streamingAssembly = useCallback(async (data: LeagueAssemblyRequest) => {
    setIsStreaming(true);
    setProgress({ type: 'progress', message: 'Starting assembly...', percent: 0 });

    try {
      const response = await leagueApi.assembleScoringStream(data);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body');
      }

      const decoder = new TextDecoder();
      
      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          break;
        }

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              setProgress(data);
              
              if (data.type === 'complete' || data.type === 'error') {
                break;
              }
            } catch (e) {
              console.warn('Failed to parse SSE data:', line);
            }
          }
        }
      }
    } catch (error) {
      console.error('Streaming assembly failed:', error);
      setProgress({ type: 'error', error: error instanceof Error ? error.message : 'Unknown error' });
    } finally {
      setIsStreaming(false);
    }
  }, []);

  return {
    assemblyMutation,
    streamingAssembly,
    progress,
    isStreaming,
    isLoading: assemblyMutation.isPending || isStreaming,
    error: assemblyMutation.error,
  };
}; 