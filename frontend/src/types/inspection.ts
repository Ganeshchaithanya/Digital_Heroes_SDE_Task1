export type Severity = 'info' | 'warning' | 'critical';
export type Category = 'seo' | 'performance' | 'accessibility' | 'content';

export interface TechnicalMetrics {
  title_length: number;
  meta_description_length: number;
  h1_count: number;
  h2_count: number;
  total_images_count: number;
  missing_alt_images_count: number;
  word_count: number;
  internal_links_count: number;
  external_links_count: number;
  response_time_ms: number;
  status_code: number;
}

export interface CategoryScores {
  seo: number;
  performance: number;
  accessibility: number;
  content: number;
  overall: number;
}

export interface IssueItem {
  issue: string;
  category: Category;
  severity: Severity;
  observed_value: string | number | boolean;
  expected_value: string;
  recommendation: string;
}

export interface AiSummary {
  executive_summary: string;
  key_strengths: string[];
  prioritized_issues: string[];
  action_plan: string[];
}

export interface InspectionResponse {
  url: string;
  technical_metrics: TechnicalMetrics;
  scores: CategoryScores;
  issues: IssueItem[];
  recommendations: string[];
  ai_summary: AiSummary | null;
}
