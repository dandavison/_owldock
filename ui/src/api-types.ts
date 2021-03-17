export interface EmployeeSerializer {
    id?: number;
    first_name: string;
    last_name: string;
    home_country: string;
}

export interface ImmigrationTaskSerializer {
    id?: number;
    case_type: string;
    created_at?: string;
    current_status: string;
    host_country: string;
    progress: number;
    service: string;
    target_entry_date: string;
    employee: any;
}

export interface ImmigrationTaskListRowSerializer {
    id?: number;
    case_type: string;
    created_at?: string;
    current_status: string;
    host_country: string;
    progress: number;
    service: string;
    target_entry_date: string;
    employee?: any;
}

