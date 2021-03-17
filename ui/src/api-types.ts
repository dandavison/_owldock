export interface PersonImmigrationTaskSerializer {
    id?: number;
    person?: any;
    case_type: string;
    current_status: string;
    host_country: string;
    progress: number;
    service: string;
    target_entry_date: string;
}

