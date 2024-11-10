"use client"

import * as React from 'react'
import { BarChart, Camera, FileVideo, Folder, Grid, Image as ImageIcon, Mic, Plus } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Textarea } from '@/components/ui/textarea'
import { Progress } from '@/components/ui/progress'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { CreateStudy } from '@/components/research/create-study'

export default function Dashboard() {
  const [activeTab, setActiveTab] = React.useState('overview')
  const [isRecording, setIsRecording] = React.useState(false)
  const [recordingMode, setRecordingMode] = React.useState('screen-webcam')
  const [aiInterviewInProgress, setAiInterviewInProgress] = React.useState(false)
  const [isCreateStudyOpen, setIsCreateStudyOpen] = React.useState(false)

  const startRecording = () => {
    setIsRecording(true)
    // Implement actual recording logic here
  }

  const startAiInterview = () => {
    setAiInterviewInProgress(true)
    // Implement AI interview logic here
  }

  const stopAiInterview = () => {
    setAiInterviewInProgress(false)
    // Implement logic to save AI interview results
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="hidden w-64 bg-white shadow-md sm:block">
        <div className="flex h-20 items-center justify-center border-b">
          <h1 className="text-2xl font-bold text-gray-800">Research Platform</h1>
        </div>
        <nav className="mt-6">
          <button
            className="flex w-full items-center px-6 py-3 text-gray-600 hover:bg-gray-100 hover:text-gray-800"
            onClick={() => setActiveTab('overview')}
          >
            <Grid className="mr-3 h-6 w-6" />
            Overview
          </button>
          <button
            className="flex w-full items-center px-6 py-3 text-gray-600 hover:bg-gray-100 hover:text-gray-800"
            onClick={() => setActiveTab('studies')}
          >
            <Folder className="mr-3 h-6 w-6" />
            Studies
          </button>
          <button
            className="flex w-full items-center px-6 py-3 text-gray-600 hover:bg-gray-100 hover:text-gray-800"
            onClick={() => setActiveTab('stimuli')}
          >
            <ImageIcon className="mr-3 h-6 w-6" />
            Stimuli
          </button>
          <button
            className="flex w-full items-center px-6 py-3 text-gray-600 hover:bg-gray-100 hover:text-gray-800"
            onClick={() => setActiveTab('recordings')}
          >
            <FileVideo className="mr-3 h-6 w-6" />
            Recordings
          </button>
          <button
            className="flex w-full items-center px-6 py-3 text-gray-600 hover:bg-gray-100 hover:text-gray-800"
            onClick={() => setActiveTab('ai-interview')}
          >
            <Mic className="mr-3 h-6 w-6" />
            AI Interview
          </button>
          <button
            className="flex w-full items-center px-6 py-3 text-gray-600 hover:bg-gray-100 hover:text-gray-800"
            onClick={() => setActiveTab('analysis')}
          >
            <BarChart className="mr-3 h-6 w-6" />
            Analysis
          </button>
        </nav>
      </div>

      {/* Main content */}
      <div className="flex-1 overflow-y-auto">
        <header className="flex h-20 items-center justify-between border-b bg-white px-6">
          <h2 className="text-2xl font-semibold text-gray-800">Dashboard</h2>
          <div className="flex items-center">
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline" className="mr-4">
                  <Camera className="mr-2 h-4 w-4" />
                  New Recording
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Start New Recording</DialogTitle>
                  <DialogDescription>
                    Choose your recording mode and start capturing.
                  </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  <div className="grid grid-cols-4 items-center gap-4">
                    <Label htmlFor="recording-mode" className="text-right">
                      Mode
                    </Label>
                    <Select
                      value={recordingMode}
                      onValueChange={(value) => setRecordingMode(value)}
                    >
                      <SelectTrigger className="col-span-3">
                        <SelectValue placeholder="Select recording mode" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="screen-webcam">Screen & Webcam</SelectItem>
                        <SelectItem value="screen-only">Screen Only</SelectItem>
                        <SelectItem value="webcam-only">Webcam Only</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <DialogFooter>
                  <Button onClick={startRecording} disabled={isRecording}>
                    Start Recording
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
            <Button onClick={() => setIsCreateStudyOpen(true)}>
              <Plus className="mr-2 h-4 w-4" />
              New Study
            </Button>
          </div>
        </header>

        <main className="p-6">
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="mb-4">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="studies">Studies</TabsTrigger>
              <TabsTrigger value="stimuli">Stimuli</TabsTrigger>
              <TabsTrigger value="recordings">Recordings</TabsTrigger>
              <TabsTrigger value="ai-interview">AI Interview</TabsTrigger>
              <TabsTrigger value="analysis">Analysis</TabsTrigger>
            </TabsList>
            <TabsContent value="overview">
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                    <CardTitle className="text-sm font-medium">Total Studies</CardTitle>
                    <Folder className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">12</div>
                    <p className="text-xs text-muted-foreground">+2 from last month</p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                    <CardTitle className="text-sm font-medium">Total Recordings</CardTitle>
                    <FileVideo className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">142</div>
                    <p className="text-xs text-muted-foreground">+24 from last month</p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                    <CardTitle className="text-sm font-medium">AI Interviews</CardTitle>
                    <Mic className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">32</div>
                    <p className="text-xs text-muted-foreground">+3 from last month</p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                    <CardTitle className="text-sm font-medium">Stimuli</CardTitle>
                    <ImageIcon className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">56</div>
                    <p className="text-xs text-muted-foreground">+8 from last month</p>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
            <TabsContent value="studies">
              <Card>
                <CardHeader>
                  <CardTitle>Studies</CardTitle>
                  <CardDescription>Manage your research studies</CardDescription>
                </CardHeader>
                <CardContent>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Title</TableHead>
                        <TableHead>Description</TableHead>
                        <TableHead>Created At</TableHead>
                        <TableHead>Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      <TableRow>
                        <TableCell>User Behavior Study</TableCell>
                        <TableCell>Analyzing user interactions with the new UI</TableCell>
                        <TableCell>2023-06-01</TableCell>
                        <TableCell>
                          <Button variant="outline" size="sm">View</Button>
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Product Feedback Study</TableCell>
                        <TableCell>Gathering user feedback on the latest features</TableCell>
                        <TableCell>2023-05-28</TableCell>
                        <TableCell>
                          <Button variant="outline" size="sm">View</Button>
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </CardContent>
                <CardFooter>
                  <Button onClick={() => setIsCreateStudyOpen(true)}>
                    <Plus className="mr-2 h-4 w-4" />
                    New Study
                  </Button>
                </CardFooter>
              </Card>
            </TabsContent>
            <TabsContent value="stimuli">
              <Card>
                <CardHeader>
                  <CardTitle>Stimuli</CardTitle>
                  <CardDescription>Manage your study stimuli</CardDescription>
                </CardHeader>
                <CardContent>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Title</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead>Study</TableHead>
                        <TableHead>Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      <TableRow>
                        <TableCell>Homepage Mockup</TableCell>
                        <TableCell>Image</TableCell>
                        <TableCell>User Behavior Study</TableCell>
                        <TableCell>
                          <Button variant="outline" size="sm">View</Button>
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Product Demo Video</TableCell>
                        <TableCell>Video</TableCell>
                        <TableCell>Product Feedback Study</TableCell>
                        <TableCell>
                          <Button variant="outline" size="sm">View</Button>
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </CardContent>
                <CardFooter>
                  <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    New Stimulus
                  </Button>
                </CardFooter>
              </Card>
            </TabsContent>
            <TabsContent value="recordings">
              <Card>
                <CardHeader>
                  <CardTitle>Recordings</CardTitle>
                  <CardDescription>Manage your research recordings</CardDescription>
                </CardHeader>
                <CardContent>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Title</TableHead>
                        <TableHead>Study</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead>Created At</TableHead>
                        <TableHead>Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      <TableRow>
                        <TableCell>User Interview 1</TableCell>
                        <TableCell>User Behavior Study</TableCell>
                        <TableCell>Screen & Webcam</TableCell>
                        <TableCell>2023-06-01</TableCell>
                        <TableCell>
                          <Button variant="outline" size="sm">View</Button>
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Usability Test 2</TableCell>
                        <TableCell>Product Feedback Study</TableCell>
                        <TableCell>Screen Only</TableCell>
                        <TableCell>2023-05-30</TableCell>
                        <TableCell>
                          <Button variant="outline" size="sm">View</Button>
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </CardContent>
                <CardFooter>
                  <Button>
                    <Camera className="mr-2 h-4 w-4" />
                    New Recording
                  </Button>
                </CardFooter>
              </Card>
            </TabsContent>
            <TabsContent value="ai-interview">
              <Card>
                <CardHeader>
                  <CardTitle>AI Interview</CardTitle>
                  <CardDescription>Conduct AI-powered interviews</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="discussion-guide">Upload Discussion Guide</Label>
                      <Input id="discussion-guide" type="file" />
                    </div>
                    <div>
                      <Label htmlFor="interview-language">Interview Language</Label>
                      <Select>
                        <SelectTrigger>
                          <SelectValue placeholder="Select language" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="en">English</SelectItem>
                          <SelectItem value="es">Spanish</SelectItem>
                          <SelectItem value="fr">French</SelectItem>
                          <SelectItem value="de">German</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Button onClick={aiInterviewInProgress ? stopAiInterview : startAiInterview}>
                        {aiInterviewInProgress ? 'Stop AI Interview' : 'Start AI Interview'}
                      </Button>
                    </div>
                    {aiInterviewInProgress && (
                      <div>
                        <Label>Interview Progress</Label>
                        <Progress value={50} className="w-full" />
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="analysis">
              <Card>
                <CardHeader>
                  <CardTitle>Analysis</CardTitle>
                  <CardDescription>Analyze your research data</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <Label htmlFor="study-select">Select Study</Label>
                      <Select>
                        <SelectTrigger>
                          <SelectValue placeholder="Choose a study" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="user-behavior">User Behavior Study</SelectItem>
                          <SelectItem value="product-feedback">Product Feedback Study</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label>Filter by:</Label>
                      <div className="flex space-x-2 mt-2">
                        <Button variant="outline">Categories</Button>
                        <Button variant="outline">Tags</Button>
                      </div>
                    </div>
                    <div>
                      <Button>
                        <BarChart className="mr-2 h-4 w-4" />
                        Generate AI Synthesis
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </main>
      </div>

      {isCreateStudyOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <CreateStudy onClose={() => setIsCreateStudyOpen(false)} />
        </div>
      )}
    </div>
  )
}