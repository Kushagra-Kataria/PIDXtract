
import React from 'react';
import Navbar from '@/components/layout/Navbar';
import DiagramViewer from '@/components/viewer/DiagramViewer';
import { Button } from "@/components/ui/button";
import { ArrowLeft, Download, Share, Save } from 'lucide-react';
import { Link } from 'react-router-dom';

const Viewer = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-grow pt-20">
        <div className="container px-4 py-6 md:px-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-4">
            <div className="flex items-center gap-4">
              <Button variant="outline" size="icon" asChild>
                <Link to="/dashboard">
                  <ArrowLeft className="h-4 w-4" />
                </Link>
              </Button>
              <div>
                <h1 className="text-2xl font-bold tracking-tight">Process Flow Diagram 001</h1>
                <p className="text-muted-foreground">Last updated: April 15, 2025</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 mr-2" />
                Export
              </Button>
              <Button variant="outline" size="sm">
                <Share className="h-4 w-4 mr-2" />
                Share
              </Button>
              <Button size="sm">
                <Save className="h-4 w-4 mr-2" />
                Save
              </Button>
            </div>
          </div>
          
          <DiagramViewer />
        </div>
      </main>
    </div>
  );
};

export default Viewer;
