export interface UserSerializer {
    first_name?: string;
    last_name?: string;
    email?: string;
}

export interface EmployeeSerializer {
    id?: number;
    created_at?: string;
    modified_at?: string;
    user?: any;
    employer?: any;
    home_country?: any;
    nationalities?: any[];
}

export interface CaseSerializer {
    id?: number;
    created_at?: string;
    modified_at?: string;
    service: string;
    target_entry_date: string;
    status: string;
    progress: number;
    client_contact?: any;
    provider_contact?: any;
    employee?: any;
    process?: any;
    host_country?: any;
}

export interface CountrySerializer {
    id?: number;
    created_at?: string;
    modified_at?: string;
    name: string;
    code: string;
    unicode_flag: string;
}

