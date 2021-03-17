export interface ImmigrationTaskSerializer {
    id?: number;
    employee?: any;
    case_type: string;
    current_status: string;
    host_country: string;
    progress: number;
    service: string;
    target_entry_date: string;
}

