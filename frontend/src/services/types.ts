export interface LeagueAssemblyRequest {
  platform: 'espn' | 'sleeper';
  league_id: string;
  s2?: string;
  swid?: string;
}

export interface LeagueAssemblyResponse {
  league_id: string;
  status: string;
}

export interface ChartData {
  teams?: string[];
  weeks?: string[];
  expected_wins?: number[];
  colors?: string[];
  // EW Difference data
  ew_difference?: number[];
  // Luck data
  likelihood?: number[];
  // Bonage data
  bi?: number[];
  // Consistency data
  consistency_scores?: number[];
  avg_points?: number[];
  // Draft analysis data
  positions?: string[];
  player_names?: string[];
  sleeper_scores?: number[];
  player_ids?: string[];
  position_picks?: number[];
  positional_ranks?: number[];
  first_initials?: string[];
  last_names?: string[];
  draft_rounds?: number[];
  avg_positional_ranks?: number[];
  // Draft injury data - complex nested structure
  draft_injury_data?: {
    draft_data?: Record<string, Array<Array<{
      name: string;
      percent_inj: number;
      id: string;
      bg_color: string;
    } | null>>>;
    team_names?: string[];
  } | Record<string, Array<Array<{
    name: string;
    percent_inj: number;
    id: string;
    bg_color: string;
  } | null>>>;
}

export interface AnalysisResponse {
  chart_data?: ChartData;
  chart_html?: string; // Keep for backward compatibility
  metadata: {
    league_id: string;
    analysis_type: string;
    chart_type: string;
    num_teams: number;
    num_weeks: number;
    summary?: {
      // EW Difference summary
      lucky_name?: string;
      l_total_wins?: number;
      l_total_ex_wins?: number;
      l_ew_diff?: number;
      unlucky_name?: string;
      u_total_wins?: number;
      u_total_ex_wins?: number;
      u_ew_diff?: number;
      // Luck summary
      l_prob?: number;
      u_prob?: number;
      perc_lucky?: number;
    };
  };
}

export interface DebugResponse {
  num_teams: number;
  num_weeks: number;
  assembly_type: string;
  teams: Record<string, {
    name: string;
    has_scores: boolean;
    has_wins: boolean;
    has_ranks: boolean;
    score_count: number;
    win_count: number;
    rank_count: number;
  }>;
}

export interface DraftProcessingResponse {
  league_id: string;
  status: string;
  platform: string;
}

export interface ProgressUpdate {
  type: 'progress' | 'complete' | 'error';
  message: string;
  percent: number;
  error?: string;
} 