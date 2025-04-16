
import React from 'react';
import Navbar from '@/components/layout/Navbar';
import HeroSection from '@/components/home/HeroSection';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScanSearch, Database, GanttChart, BrainCircuit } from 'lucide-react';

const Index = () => {
  const features = [
    {
      title: 'Smart Recognition',
      description: 'Advanced computer vision algorithms identify and classify symbols, lines, and annotations in P&ID diagrams.',
      icon: ScanSearch,
    },
    {
      title: 'Metadata Extraction',
      description: 'Extract equipment tags, specifications, connections, and other critical information automatically.',
      icon: Database,
    },
    {
      title: 'Interactive Visualization',
      description: 'Navigate complex diagrams with our intuitive interface featuring zoom, pan, and interactive overlays.',
      icon: GanttChart,
    },
    {
      title: 'AI-Powered Analysis',
      description: 'Leverage machine learning to detect patterns, identify inconsistencies, and enhance diagram completeness.',
      icon: BrainCircuit,
    },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-grow">
        <HeroSection />
        
        <section className="py-12 md:py-24">
          <div className="container px-4 md:px-6">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold tracking-tight">Powerful Features</h2>
              <p className="text-muted-foreground mt-4 max-w-2xl mx-auto">
                Our platform combines cutting-edge AI with intuitive design to transform how you work with P&ID diagrams.
              </p>
            </div>
            
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {features.map((feature, index) => (
                <Card key={index} className="border-border overflow-hidden">
                  <CardHeader className="pb-3">
                    <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center mb-3">
                      <feature.icon className="h-6 w-6 text-primary" />
                    </div>
                    <CardTitle className="text-xl">{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground text-sm">{feature.description}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>
        
        <section className="py-12 md:py-24 bg-muted/30">
          <div className="container px-4 md:px-6">
            <div className="grid gap-8 md:grid-cols-2 md:gap-12">
              <div>
                <h2 className="text-3xl font-bold tracking-tight mb-4">Streamline Engineering Documentation</h2>
                <p className="text-muted-foreground mb-6">
                  PIDXtract transforms static engineering diagrams into searchable, interactive, and intelligent digital assets.
                </p>
                <ul className="space-y-2">
                  {[
                    'Save hundreds of hours manually interpreting P&IDs',
                    'Eliminate human error in data extraction',
                    'Create searchable databases from your diagram library',
                    'Generate reports and exports with a single click',
                    'Integrate with your existing engineering tools',
                  ].map((item, index) => (
                    <li key={index} className="flex items-start">
                      <div className="h-5 w-5 rounded-full bg-primary/20 flex items-center justify-center mr-2 mt-0.5">
                        <div className="h-2 w-2 rounded-full bg-primary"></div>
                      </div>
                      <span className="text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="relative">
                <div className="absolute -inset-4 md:-inset-6 bg-gradient-to-r from-primary/5 to-secondary/5 rounded-xl"></div>
                <div className="relative h-full rounded-xl overflow-hidden border bg-card p-2">
                  <div className="h-full rounded-lg overflow-hidden bg-muted/50 flex items-center justify-center">
                    <div className="animate-pulse text-center p-8">
                      <div className="h-48 w-full max-w-sm rounded-md bg-muted mb-4 mx-auto"></div>
                      <div className="h-4 w-3/4 rounded-md bg-muted mb-2 mx-auto"></div>
                      <div className="h-4 w-1/2 rounded-md bg-muted mx-auto"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
      
      <footer className="border-t py-8 bg-card">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center mb-4 md:mb-0">
              <div className="flex items-center justify-center w-8 h-8 rounded-md bg-primary text-primary-foreground font-bold mr-2">
                PX
              </div>
              <span className="font-bold">PIDXtract</span>
            </div>
            <div className="text-sm text-muted-foreground">
              © 2025 PIDXtract. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
