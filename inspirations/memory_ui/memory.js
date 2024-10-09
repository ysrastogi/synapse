import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

const SharedMemoryDashboard = () => {
  const [nodes, setNodes] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [cacheUsage, setCacheUsage] = useState([]);
  const [versions, setVersions] = useState([]);
  const [keys, setKeys] = useState([]);
  const [memoryAllocation, setMemoryAllocation] = useState(0);
  const [gpuEnabled, setGpuEnabled] = useState(false);

  useEffect(() => {
    // Fetch initial data
    fetchNodes();
    fetchCacheUsage();
    fetchVersions();
    fetchKeys();
  }, []);

  const fetchNodes = () => {
    // Simulated API call
    setNodes(['Node 1', 'Node 2', 'Node 3']);
  };

  const fetchCacheUsage = () => {
    // Simulated API call
    setCacheUsage([
      { name: 'Node 1', used: 75, total: 100 },
      { name: 'Node 2', used: 50, total: 100 },
      { name: 'Node 3', used: 25, total: 100 },
    ]);
  };

  const fetchVersions = () => {
    // Simulated API call
    setVersions([
      { key: 'key1', versions: ['v1', 'v2', 'v3'] },
      { key: 'key2', versions: ['v1', 'v2'] },
    ]);
  };

  const fetchKeys = () => {
    // Simulated API call
    setKeys(['key1', 'key2', 'key3', 'key4']);
  };

  const handleNodeSelect = (node) => {
    setSelectedNode(node);
    // Fetch node-specific data here
  };

  const handleMemoryAllocation = (value) => {
    setMemoryAllocation(value);
    // API call to update memory allocation
  };

  const handleGpuToggle = () => {
    setGpuEnabled(!gpuEnabled);
    // API call to update GPU configuration
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Shared Memory System Dashboard</h1>
      
      <Tabs defaultValue="overview" className="w-full">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="nodes">Nodes</TabsTrigger>
          <TabsTrigger value="versions">Versions</TabsTrigger>
          <TabsTrigger value="keys">Keys</TabsTrigger>
          <TabsTrigger value="config">Configuration</TabsTrigger>
        </TabsList>
        
        <TabsContent value="overview">
          <Card>
            <CardHeader>
              <CardTitle>System Overview</CardTitle>
              <CardDescription>Cache usage across all nodes</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={cacheUsage}>
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="used" fill="#8884d8" name="Used Cache" />
                  <Bar dataKey="total" fill="#82ca9d" name="Total Cache" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="nodes">
          <Card>
            <CardHeader>
              <CardTitle>Node Management</CardTitle>
              <CardDescription>Select a node to view details</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex space-x-2">
                {nodes.map((node) => (
                  <Button key={node} onClick={() => handleNodeSelect(node)}>
                    {node}
                  </Button>
                ))}
              </div>
              {selectedNode && (
                <div className="mt-4">
                  <h3 className="text-lg font-semibold">Node: {selectedNode}</h3>
                  {/* Add node-specific information here */}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="versions">
          <Card>
            <CardHeader>
              <CardTitle>Version History</CardTitle>
              <CardDescription>View versions for each key</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Key</TableHead>
                    <TableHead>Versions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {versions.map((item) => (
                    <TableRow key={item.key}>
                      <TableCell>{item.key}</TableCell>
                      <TableCell>{item.versions.join(', ')}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="keys">
          <Card>
            <CardHeader>
              <CardTitle>Keys</CardTitle>
              <CardDescription>List of all keys in the system</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="list-disc pl-5">
                {keys.map((key) => (
                  <li key={key}>{key}</li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="config">
          <Card>
            <CardHeader>
              <CardTitle>System Configuration</CardTitle>
              <CardDescription>Manage system resources and settings</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Memory Allocation (GB)</label>
                  <Input
                    type="number"
                    value={memoryAllocation}
                    onChange={(e) => handleMemoryAllocation(e.target.value)}
                    className="mt-1"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Enable GPU</label>
                  <Button onClick={handleGpuToggle} variant={gpuEnabled ? "default" : "secondary"}>
                    {gpuEnabled ? 'Enabled' : 'Disabled'}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default SharedMemoryDashboard;