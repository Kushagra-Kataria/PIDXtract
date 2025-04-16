
import React from 'react';
import Navbar from '@/components/layout/Navbar';
import FileUploader from '@/components/dashboard/FileUploader';
import DiagramsList from '@/components/dashboard/DiagramsList';
import { Button } from "@/components/ui/button";
import { FileText, FileUp, BrainCircuit, Database } from 'lucide-react';

const Dashboard = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-grow pt-20">
        <div className="container px-4 py-6 md:py-10 md:px-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
              <p className="text-muted-foreground mt-1">
                Manage and analyze your P&ID diagrams
              </p>
            </div>
            <div className="flex items-center gap-2 mt-4 md:mt-0">
              <Button variant="outline" className="gap-2">
                <FileText className="h-4 w-4" />
                Export Data
              </Button>
              <Button className="gap-2">
                <FileUp className="h-4 w-4" />
                Upload New
              </Button>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {[
              { title: 'Total Diagrams', value: '12', icon: FileText, color: 'primary' },
              { title: 'Processing', value: '1', icon: BrainCircuit, color: 'yellow-500' },
              { title: 'Completed', value: '10', icon: Database, color: 'green-500' },
              { title: 'Failed', value: '1', icon: FileText, color: 'red-500' },
            ].map((stat, index) => (
              <div key={index} className="bg-card rounded-lg border p-6">
                <div className="flex items-center gap-4">
                  <div className={`h-12 w-12 rounded-full bg-${stat.color}/10 flex items-center justify-center`}>
                    <stat.icon className={`h-6 w-6 text-${stat.color}`} />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">{stat.title}</p>
                    <h3 className="text-2xl font-bold">{stat.value}</h3>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mb-8">
            <FileUploader />
          </div>
          
          <div>
            <DiagramsList />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
