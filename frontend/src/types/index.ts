export interface DiseaseInfo {
    disease: string;
    description: string | null;
    workout: string | null;
    precautions: string | null;
    diet: string | null;
}

export interface DiagnosisResponse {
    symptoms: string[];
    disease_info: DiseaseInfo;
    additional_info: string;
    wikipedia_image?: string;
}

export interface ChatMessage {
    id: string;
    text: string;
    sender: 'user' | 'bot';
    timestamp: Date;
    diagnosis?: DiagnosisResponse;
} 