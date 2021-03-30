import { ApplicantSerializer } from "./api-types";

export function applicantUnicodeFlags(applicant: ApplicantSerializer): string {
  return applicant.nationalities
    .map(nationality => nationality.unicode_flag)
    .join(" ");
}
