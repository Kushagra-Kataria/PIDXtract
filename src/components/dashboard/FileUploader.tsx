
import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Upload, FileText, AlertCircle } from 'lucide-react';
import { useToast } from "@/components/ui/use-toast";

const FileUploader = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const { toast } = useToast();

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFiles(files);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(e.target.files);
    }
  };

  const handleFiles = (files: FileList) => {
    setIsUploading(true);
    setProgress(0);
    
    // Simulate upload progress
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsUploading(false);
          toast({
            title: "Upload Complete",
            description: "Your P&ID diagram is now being processed.",
          });
          return 100;
        }
        return prev + 5;
      });
    }, 300);
  };

  return (
    <Card className={`border ${isDragging ? 'border-primary' : 'border-border'} transition-colors`}>
      <CardContent className="p-6">
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`
            flex flex-col items-center justify-center p-8 rounded-md
            border-2 border-dashed transition-all
            ${isDragging ? 'border-primary bg-primary/5' : 'border-muted'}
            ${isUploading ? 'opacity-60 pointer-events-none' : 'cursor-pointer'}
          `}
        >
          <input
            type="file"
            id="file-upload"
            className="hidden"
            accept=".pdf,.png,.jpg,.jpeg,.svg,.dwg"
            onChange={handleFileSelect}
            disabled={isUploading}
          />
          
          {isUploading ? (
            <div className="w-full space-y-4">
              <div className="flex justify-between text-sm">
                <span>Uploading...</span>
                <span>{progress}%</span>
              </div>
              <Progress value={progress} />
            </div>
          ) : (
            <>
              <div className="h-16 w-16 rounded-full bg-muted/50 flex items-center justify-center mb-4">
                <Upload className="h-8 w-8 text-muted-foreground" />
              </div>
              <h3 className="text-lg font-medium mb-2">Upload P&ID Diagram</h3>
              <p className="text-sm text-muted-foreground text-center mb-6">
                Drag and drop your files here, or click to browse
              </p>
              <Button asChild>
                <label htmlFor="file-upload" className="cursor-pointer">
                  <FileText className="mr-2 h-4 w-4" />
                  Browse Files
                </label>
              </Button>
            </>
          )}
        </div>
        
        {!isUploading && (
          <div className="flex items-center mt-4 text-xs text-muted-foreground">
            <AlertCircle className="h-3 w-3 mr-1" />
            <span>Supported formats: PDF, PNG, JPG, SVG, DWG</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default FileUploader;
