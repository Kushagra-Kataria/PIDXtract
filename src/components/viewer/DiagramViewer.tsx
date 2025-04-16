
import React, { useState, useRef, useEffect } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ZoomIn, ZoomOut, RotateCw, Maximize, Layers, Tag, Info } from 'lucide-react';

const DiagramViewer = () => {
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const containerRef = useRef<HTMLDivElement>(null);

  const handleZoomIn = () => {
    setScale(prev => Math.min(prev + 0.1, 2));
  };

  const handleZoomOut = () => {
    setScale(prev => Math.max(prev - 0.1, 0.5));
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    setDragStart({
      x: e.clientX - position.x,
      y: e.clientY - position.y
    });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (isDragging) {
      setPosition({
        x: e.clientX - dragStart.x,
        y: e.clientY - dragStart.y
      });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleReset = () => {
    setScale(1);
    setPosition({ x: 0, y: 0 });
  };

  // Mock data for the placeholder diagram
  const mockSymbols = [
    { id: 1, x: 120, y: 200, type: 'valve' },
    { id: 2, x: 230, y: 150, type: 'pump' },
    { id: 3, x: 320, y: 220, type: 'instrument' },
    { id: 4, x: 180, y: 300, type: 'vessel' },
  ];

  useEffect(() => {
    const handleMouseLeave = () => {
      setIsDragging(false);
    };

    const container = containerRef.current;
    if (container) {
      container.addEventListener('mouseleave', handleMouseLeave);
    }

    return () => {
      if (container) {
        container.removeEventListener('mouseleave', handleMouseLeave);
      }
    };
  }, []);

  return (
    <Card className="h-[calc(100vh-240px)] flex flex-col overflow-hidden">
      <div className="p-4 border-b flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Button variant="outline" size="icon" onClick={handleZoomIn}>
            <ZoomIn className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="icon" onClick={handleZoomOut}>
            <ZoomOut className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="icon" onClick={handleReset}>
            <RotateCw className="h-4 w-4" />
          </Button>
          <div className="text-sm text-muted-foreground">
            Zoom: {Math.round(scale * 100)}%
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Layers className="h-4 w-4 mr-1" />
            Overlays
          </Button>
          <Button variant="outline" size="icon">
            <Maximize className="h-4 w-4" />
          </Button>
        </div>
      </div>
      <CardContent className="p-0 flex-grow flex overflow-hidden">
        <div className="flex-grow overflow-hidden grid-bg relative" 
          ref={containerRef}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          style={{ cursor: isDragging ? 'grabbing' : 'grab' }}
        >
          <div 
            className="absolute"
            style={{ 
              transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`,
              transformOrigin: 'center',
              transition: 'transform 0.1s ease',
            }}
          >
            {/* Placeholder for diagram - in a real app, you'd render the actual diagram here */}
            <div className="w-[800px] h-[600px] bg-muted/20 border border-border rounded-md relative">
              {/* Mock grid for diagram */}
              <div className="absolute inset-0 grid-bg opacity-50"></div>
              
              {/* Mock lines */}
              <svg className="absolute inset-0 w-full h-full">
                <line x1="100" y1="200" x2="400" y2="200" stroke="hsl(var(--primary))" strokeWidth="2" />
                <line x1="230" y1="150" x2="230" y2="300" stroke="hsl(var(--primary))" strokeWidth="2" />
                <line x1="320" y1="220" x2="400" y2="220" stroke="hsl(var(--primary))" strokeWidth="2" />
              </svg>
              
              {/* Mock symbols */}
              {mockSymbols.map(symbol => (
                <div 
                  key={symbol.id}
                  className="absolute w-10 h-10 bg-card border border-primary rounded-md flex items-center justify-center"
                  style={{ left: symbol.x, top: symbol.y, transform: 'translate(-50%, -50%)' }}
                >
                  <div className="text-xs font-mono text-primary">{symbol.type.substring(0, 2).toUpperCase()}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="w-80 border-l flex flex-col">
          <Tabs defaultValue="metadata" className="h-full flex flex-col">
            <TabsList className="grid grid-cols-3 mx-4 mt-4">
              <TabsTrigger value="metadata">
                <Info className="h-4 w-4 mr-1" />
                Info
              </TabsTrigger>
              <TabsTrigger value="symbols">
                <Tag className="h-4 w-4 mr-1" />
                Symbols
              </TabsTrigger>
              <TabsTrigger value="layers">
                <Layers className="h-4 w-4 mr-1" />
                Layers
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="metadata" className="flex-grow p-4 overflow-auto">
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">Diagram Title</h3>
                  <p className="text-sm">Process Flow Diagram 001</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">Document Number</h3>
                  <p className="text-sm">PID-2025-001</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">Revision</h3>
                  <p className="text-sm">A</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">Date</h3>
                  <p className="text-sm">2025-04-15</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">Project</h3>
                  <p className="text-sm">Chemical Plant Expansion</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-1">Client</h3>
                  <p className="text-sm">ABC Chemical Corporation</p>
                </div>
                <div className="border-t pt-4">
                  <h3 className="text-sm font-medium mb-2">Extracted Information</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Valves</span>
                      <span className="font-medium">12</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Instruments</span>
                      <span className="font-medium">8</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Pumps</span>
                      <span className="font-medium">3</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Vessels</span>
                      <span className="font-medium">2</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>Pipes</span>
                      <span className="font-medium">24</span>
                    </div>
                  </div>
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="symbols" className="flex-grow p-4 overflow-auto">
              <div className="space-y-4">
                <div className="relative">
                  <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    type="search"
                    placeholder="Search symbols..."
                    className="pl-8"
                  />
                </div>
                
                <div className="space-y-2">
                  {mockSymbols.map(symbol => (
                    <div key={symbol.id} className="p-2 rounded-md hover:bg-muted/50 cursor-pointer">
                      <div className="flex items-center">
                        <div className="w-8 h-8 flex items-center justify-center bg-card border border-border rounded mr-2">
                          <span className="text-xs font-mono">{symbol.type.substring(0, 2).toUpperCase()}</span>
                        </div>
                        <div className="flex-grow">
                          <div className="text-sm font-medium capitalize">{symbol.type}</div>
                          <div className="text-xs text-muted-foreground">ID: {symbol.id}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="layers" className="flex-grow p-4 overflow-auto">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-3 h-3 rounded-full bg-primary mr-2"></div>
                    <span className="text-sm">Process Lines</span>
                  </div>
                  <Button variant="ghost" size="sm">Toggle</Button>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-3 h-3 rounded-full bg-secondary mr-2"></div>
                    <span className="text-sm">Instruments</span>
                  </div>
                  <Button variant="ghost" size="sm">Toggle</Button>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-3 h-3 rounded-full bg-accent mr-2"></div>
                    <span className="text-sm">Equipment</span>
                  </div>
                  <Button variant="ghost" size="sm">Toggle</Button>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-3 h-3 rounded-full bg-muted-foreground mr-2"></div>
                    <span className="text-sm">Annotations</span>
                  </div>
                  <Button variant="ghost" size="sm">Toggle</Button>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </CardContent>
    </Card>
  );
};

export default DiagramViewer;
