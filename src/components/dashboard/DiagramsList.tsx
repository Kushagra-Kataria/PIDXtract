
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Search, FileText, Download, Eye, Filter } from 'lucide-react';
import { Input } from "@/components/ui/input";

type DiagramStatus = 'processing' | 'complete' | 'failed';

interface Diagram {
  id: string;
  name: string;
  date: string;
  status: DiagramStatus;
  type: string;
  size: string;
}

const DIAGRAMS_DATA: Diagram[] = [
  {
    id: '1',
    name: 'Process Flow Diagram 001',
    date: '2025-04-15',
    status: 'complete',
    type: 'PDF',
    size: '2.4 MB',
  },
  {
    id: '2',
    name: 'Utility System P&ID',
    date: '2025-04-14',
    status: 'complete',
    type: 'PDF',
    size: '3.1 MB',
  },
  {
    id: '3',
    name: 'Gas Compression System',
    date: '2025-04-12',
    status: 'processing',
    type: 'DWG',
    size: '5.7 MB',
  },
  {
    id: '4',
    name: 'Water Treatment P&ID',
    date: '2025-04-10',
    status: 'failed',
    type: 'PNG',
    size: '1.2 MB',
  }
];

const DiagramsList = () => {
  const getStatusBadge = (status: DiagramStatus) => {
    switch (status) {
      case 'processing':
        return <Badge variant="outline" className="bg-yellow-500/10 text-yellow-500 border-yellow-500/20">Processing</Badge>;
      case 'complete':
        return <Badge variant="outline" className="bg-green-500/10 text-green-500 border-green-500/20">Complete</Badge>;
      case 'failed':
        return <Badge variant="outline" className="bg-red-500/10 text-red-500 border-red-500/20">Failed</Badge>;
      default:
        return null;
    }
  };

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <CardTitle>Your Diagrams</CardTitle>
          <div className="flex items-center gap-2">
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Search diagrams..."
                className="pl-8 w-full md:w-[200px] lg:w-[300px]"
              />
            </div>
            <Button variant="outline" size="icon">
              <Filter className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Size</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {DIAGRAMS_DATA.map((diagram) => (
                <TableRow key={diagram.id}>
                  <TableCell className="font-medium">
                    <div className="flex items-center gap-2">
                      <FileText className="h-4 w-4 text-muted-foreground" />
                      {diagram.name}
                    </div>
                  </TableCell>
                  <TableCell>{diagram.date}</TableCell>
                  <TableCell>{getStatusBadge(diagram.status)}</TableCell>
                  <TableCell>{diagram.type}</TableCell>
                  <TableCell>{diagram.size}</TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button variant="ghost" size="icon" disabled={diagram.status !== 'complete'}>
                        <Eye className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="icon" disabled={diagram.status !== 'complete'}>
                        <Download className="h-4 w-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
};

export default DiagramsList;
