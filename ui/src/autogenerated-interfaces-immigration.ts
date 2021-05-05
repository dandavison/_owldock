export interface OccupationSerializer {
    name: string;
}

export interface MoveSerializer {
    host_country: any;
    target_entry_date?: string;
    target_exit_date?: string;
}

export interface RouteSerializer {
    id?: number;
    host_country: any;
    uuid?: string;
    created_at?: string;
    modified_at?: string;
    name: string;
}

export interface ProcessStepSerializer {
    id?: number;
    uuid?: string;
    created_at?: string;
    modified_at?: string;
    name: string;
    sequence_number: number;
    government_fee?: number;
    estimated_min_duration_days: number;
    estimated_max_duration_days: number;
    applicant_can_enter_host_country_after?: boolean;
    applicant_can_work_in_host_country_after?: boolean;
    required_only_if_payroll_location?: any;
    required_only_if_duration_exceeds?: number;
    process_rule_set: any;
    issued_documents?: any[];
    required_only_if_nationalities?: any[];
}

export interface ProcessSerializer {
    route: RouteSerializer;
    steps: ProcessStepSerializer[];
}

