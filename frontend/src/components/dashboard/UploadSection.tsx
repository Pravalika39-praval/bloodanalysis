import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Upload, FileText } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { reportsAPI } from "@/services/api";

interface UploadSectionProps {
  onAnalysisComplete: (params: Record<string, number>) => void;
}

const UploadSection = ({ onAnalysisComplete }: UploadSectionProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const { toast } = useToast();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      toast({
        variant: "destructive",
        title: "No file selected",
        description: "Please select a blood report file to upload.",
      });
      return;
    }

    setIsProcessing(true);
    try {
      const result = await reportsAPI.uploadReport(file);
      
      onAnalysisComplete(result.extracted_parameters);
      
      toast({
        title: "Report uploaded successfully",
        description: "Your blood report has been processed and is ready for analysis.",
      });
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Upload failed",
        description: error.message || "There was an error processing your file. Please try again.",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <Card className="shadow-card hover:shadow-elegant transition-shadow duration-300">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="h-5 w-5 text-primary" />
          Upload Blood Report
        </CardTitle>
        <CardDescription>
          Upload your blood report in PDF, JPG, or PNG format (Max 10MB)
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="report-file">Select Report File</Label>
          <div className="flex items-center gap-4">
            <Input
              id="report-file"
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              onChange={handleFileChange}
              disabled={isProcessing}
              className="flex-1"
            />
            {file && (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <FileText className="h-4 w-4" />
                <span className="truncate max-w-[200px]">{file.name}</span>
              </div>
            )}
          </div>
        </div>
        
        <Button 
          onClick={handleUpload} 
          disabled={!file || isProcessing}
          className="w-full"
          size="lg"
        >
          {isProcessing ? (
            <>Processing Report...</>
          ) : (
            <>
              <Upload className="mr-2 h-5 w-5" />
              Upload and Analyze Report
            </>
          )}
        </Button>
      </CardContent>
    </Card>
  );
};

export default UploadSection;
