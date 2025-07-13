import { useQuery, useMutation } from '@tanstack/react-query';
import { leagueApi } from '../services/api';

export const useAnalysisData = (leagueId: string | null) => {
  // Scoring Analysis Queries
  const expectedWinsQuery = useQuery({
    queryKey: ['expected-wins', leagueId],
    queryFn: () => leagueApi.getExpectedWins(leagueId!),
    enabled: !!leagueId,
  });

  const ewDifferenceQuery = useQuery({
    queryKey: ['ew-difference', leagueId],
    queryFn: () => leagueApi.getEWDifference(leagueId!),
    enabled: !!leagueId,
  });

  const luckQuery = useQuery({
    queryKey: ['luck', leagueId],
    queryFn: () => leagueApi.getLuckAnalysis(leagueId!),
    enabled: !!leagueId,
  });

  const bonageQuery = useQuery({
    queryKey: ['bonage', leagueId],
    queryFn: () => leagueApi.getBonageAnalysis(leagueId!),
    enabled: !!leagueId,
  });

  const consistencyQuery = useQuery({
    queryKey: ['consistency', leagueId],
    queryFn: () => leagueApi.getConsistencyAnalysis(leagueId!),
    enabled: !!leagueId,
  });

  // Draft Analysis Queries
  const sleepersQuery = useQuery({
    queryKey: ['sleepers', leagueId],
    queryFn: () => leagueApi.getSleepers(leagueId!),
    enabled: !!leagueId,
  });

  const positionalRanksQuery = useQuery({
    queryKey: ['positional-ranks', leagueId],
    queryFn: () => leagueApi.getPositionalRanks(leagueId!),
    enabled: !!leagueId,
  });

  const draftInjuryQuery = useQuery({
    queryKey: ['draft-injury', leagueId],
    queryFn: () => leagueApi.getDraftInjury(leagueId!),
    enabled: !!leagueId,
  });

  // Draft Processing Mutation
  const processDraftMutation = useMutation({
    mutationFn: leagueApi.processDraft,
    onSuccess: () => {
      // Invalidate draft-related queries
      // This would need to be done with a queryClient instance
    },
  });

  return {
    // Scoring Analysis
    expectedWins: expectedWinsQuery,
    ewDifference: ewDifferenceQuery,
    luck: luckQuery,
    bonage: bonageQuery,
    consistency: consistencyQuery,
    
    // Draft Analysis
    sleepers: sleepersQuery,
    positionalRanks: positionalRanksQuery,
    draftInjury: draftInjuryQuery,
    
    // Draft Processing
    processDraft: processDraftMutation,
  };
}; 