
import React from 'react';
import { Button } from "@/components/ui/button";
import { ChevronRight, Upload } from 'lucide-react';
import { Link } from 'react-router-dom';

const HeroSection = () => {
  return (
    <section className="relative overflow-hidden pt-24 pb-16 md:pt-32 md:pb-24">
      <div className="absolute inset-0 grid-bg opacity-20"></div>
      <div className="absolute top-0 left-0 right-0 h-[500px] bg-gradient-radial from-secondary/10 via-transparent to-transparent"></div>
      
      <div className="container relative px-4 md:px-6">
        <div className="grid gap-6 lg:grid-cols-[1fr_400px] lg:gap-12 xl:grid-cols-[1fr_600px]">
          <div className="flex flex-col justify-center space-y-4">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none">
                Extract Intelligence from <span className="text-gradient">P&ID Diagrams</span>
              </h1>
              <p className="max-w-[600px] text-muted-foreground md:text-xl">
                Our AI-powered platform automatically extracts, categorizes, and indexes data from P&ID diagrams, making them searchable and actionable.
              </p>
            </div>
            <div className="flex flex-col gap-2 min-[400px]:flex-row">
              <Button asChild size="lg" className="h-12 px-6">
                <Link to="/dashboard">
                  <Upload className="mr-2 h-5 w-5" />
                  Upload Diagram
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="h-12 px-6">
                <Link to="/docs">
                  Learn More
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
            <div className="flex items-center space-x-4 text-sm text-muted-foreground">
              <div className="flex items-center space-x-1">
                <div className="h-2 w-2 rounded-full bg-green-500"></div>
                <span>Fast Processing</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="h-2 w-2 rounded-full bg-primary"></div>
                <span>99.8% Accuracy</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="h-2 w-2 rounded-full bg-secondary"></div>
                <span>Secure Data</span>
              </div>
            </div>
          </div>
          
          <div className="flex items-center justify-center">
            <div className="relative aspect-video overflow-hidden rounded-lg border bg-muted p-2">
              <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-secondary/20 opacity-50"></div>
              <div className="absolute inset-[2px] rounded-md bg-card flex items-center justify-center">
                <div className="text-center">
                  <div className="animate-pulse rounded-md bg-muted h-48 w-full max-w-sm mb-4"></div>
                  <div className="animate-pulse rounded-md bg-muted h-8 w-3/4 mx-auto"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
