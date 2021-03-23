export interface EmployeeSerializer {
    id?: number;
    created_at?: string;
    modified_at?: string;
    home_country: string;
    user?: any;
    employer?: any;
}

export interface CaseSerializer {
    id?: number;
    created_at?: string;
    modified_at?: string;
    service: string;
    host_country: string;
    target_entry_date: string;
    status: string;
    progress: number;
    client_contact?: any;
    provider_contact?: any;
    employee?: any;
    process?: any;
}

