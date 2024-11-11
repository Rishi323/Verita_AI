"use client"

import * as React from "react"
import { Brain, Calendar, DollarSign, Edit, Globe, GripVertical, Mail, MessageSquare, Mic, Plus, Star, Trash2, Upload, Users, Play } from "lucide-react"
import { Button } from "/Users/aryanmishra/Verita_AI/dashboard/src/components/ui/button.tsx"
import { Card, CardContent, CardHeader, CardTitle } from "/Users/aryanmishra/Verita_AI/dashboard/src/components/ui/card.tsx"
import { Input } from "/Users/aryanmishra/Verita_AI/dashboard/src/components/ui/input.tsx"
import { Label } from "/Users/aryanmishra/Verita_AI/dashboard/src/components/ui/label.tsx"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "/Users/aryanmishra/Verita_AI/dashboard/src/components/ui/tabs.tsx"
import { Textarea } from "/Users/aryanmishra/Verita_AI/dashboard/src/components/ui/Textarea.tsx"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "/Users/aryanmishra/Verita_AI/dashboard/src/components/ui/select.tsx"
import { Slider } from "/Users/aryanmishra/Verita_AI/dashboard/src/components/ui/slider.tsx"
import { Switch } from "/Users/aryanmishra/Verita_AI/dashboard/src/components/ui/switch.tsx"
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "/Users/aryanmishra/Verita_AI/dashboard/src/components/ui/command.tsx"
import { Popover, PopoverContent, PopoverTrigger } from "/Users/aryanmishra/Verita_AI/dashboard/src/components/ui/Popover.tsx"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "/Users/aryanmishra/Verita_AI/dashboard/src/components/ui/table.tsx"
import type { CreateStudyProps, Question, ScreenerQuestion, User } from "/Users/aryanmishra/Verita_AI/dashboard/src/research.ts"

interface AIPromptInputProps {
  placeholder: string
  suggestions: string[]
}

const AIPromptInput: React.FC<AIPromptInputProps> = ({ placeholder, suggestions }) => (
  <Popover>
    <PopoverTrigger asChild>
      <Input placeholder={placeholder} />
    </PopoverTrigger>
    <PopoverContent className="w-[300px] p-0">
      <Command>
        <CommandInput placeholder="Search suggestions..." />
        <CommandList>
          <CommandEmpty>No suggestions found.</CommandEmpty>
          <CommandGroup>
            {suggestions.map((suggestion, index) => (
              <CommandItem key={index} onSelect={() => console.log(suggestion)}>
                {suggestion}
              </CommandItem>
            ))}
          </CommandGroup>
        </CommandList>
      </Command>
    </PopoverContent>
  </Popover>
)

export function CreateStudy({ onClose }: CreateStudyProps) {
  const [questions, setQuestions] = React.useState<Question[]>([
    { id: 1, text: "What's your experience with our product?", important: false, topic: "Product Experience" },
    { id: 2, text: "How often do you use similar products?", important: true, topic: "Usage Patterns" },
    { id: 3, text: "What features would you like to see improved?", important: false, topic: "Feature Requests" },
  ])

  const [screenerQuestions, setScreenerQuestions] = React.useState<ScreenerQuestion[]>([
    { id: 1, text: "How frequently do you use our product?" },
    { id: 2, text: "What is your primary use case for our product?" },
  ])

  const [screenedUsers, setScreenedUsers] = React.useState<User[]>([
    { id: 1, name: "John Doe", age: 28, gender: "Male", income: "Medium" },
    { id: 2, name: "Jane Smith", age: 35, gender: "Female", income: "High" },
    { id: 3, name: "Alex Johnson", age: 22, gender: "Non-binary", income: "Low" },
  ])

  const [finalUsers, setFinalUsers] = React.useState<User[]>([
    { id: 1, name: "John Doe", age: 28, gender: "Male", income: "Medium" },
    { id: 2, name: "Jane Smith", age: 35, gender: "Female", income: "High" },
  ])

  const addQuestion = (topic: string) => {
    const newId = Math.max(...questions.map(q => q.id)) + 1
    setQuestions([...questions, { id: newId, text: "", important: false, topic }])
  }

  const removeQuestion = (id: number) => {
    setQuestions(questions.filter(q => q.id !== id))
  }

  const toggleImportant = (id: number) => {
    setQuestions(questions.map(q => q.id === id ? { ...q, important: !q.important } : q))
  }

  const updateQuestion = (id: number, text: string) => {
    setQuestions(questions.map(q => q.id === id ? { ...q, text } : q))
  }

  const groupedQuestions = questions.reduce((acc, question) => {
    if (!acc[question.topic]) {
      acc[question.topic] = []
    }
    acc[question.topic].push(question)
    return acc
  }, {} as Record<string, Question[]>)

  return (
    <div className="flex flex-col gap-6 p-6 bg-white rounded-lg shadow-lg max-w-4xl mx-auto overflow-y-auto max-h-[90vh]">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Create New Study</h1>
          <p className="text-sm text-muted-foreground">
            Set up your research study with AI assistance
          </p>
        </div>
        <Button onClick={onClose}>Close</Button>
      </div>

      <Tabs defaultValue="guide" className="w-full">
        <TabsList>
          <TabsTrigger value="guide">Discussion Guide</TabsTrigger>
          <TabsTrigger value="edit">Edit Guide</TabsTrigger>
          <TabsTrigger value="logistics">Logistics</TabsTrigger>
          <TabsTrigger value="stimuli">Stimuli</TabsTrigger>
          <TabsTrigger value="ai-interview">AI Interview</TabsTrigger>
        </TabsList>

        <TabsContent value="guide" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Brain className="h-5 w-5" />
                AI-Generated Discussion Guide
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="study-topic">Topic of the Study</Label>
                <AIPromptInput
                  placeholder="E.g., User experience of our mobile app"
                  suggestions={[
                    "User onboarding experience",
                    "Feature adoption rates",
                    "Customer satisfaction survey",
                  ]}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="framework">Research Framework</Label>
                <Select>
                  <SelectTrigger id="framework">
                    <SelectValue placeholder="Select a framework" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="thematic">Thematic Analysis</SelectItem>
                    <SelectItem value="grounded">Grounded Theory</SelectItem>
                    <SelectItem value="phenomenological">Phenomenological</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="setting">Interview Setting</Label>
                <Select>
                  <SelectTrigger id="setting">
                    <SelectValue placeholder="Select a setting" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="in-person">In-person</SelectItem>
                    <SelectItem value="video-call">Video Call</SelectItem>
                    <SelectItem value="phone">Phone</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="interview-type">Interview Type</Label>
                <Select>
                  <SelectTrigger id="interview-type">
                    <SelectValue placeholder="Select interview type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ai-moderated">AI-Moderated</SelectItem>
                    <SelectItem value="ux-researcher">UX Researcher Conducted</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="length">Interview Length (minutes)</Label>
                <Slider
                  id="length"
                  min={15}
                  max={120}
                  step={15}
                  defaultValue={[60]}
                  className="w-full"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="topics">Interview Topics to Focus On</Label>
                <AIPromptInput
                  placeholder="E.g., Onboarding experience, Feature usability, Overall satisfaction"
                  suggestions={[
                    "User interface design",
                    "Performance and speed",
                    "Integration with other tools",
                    "Customer support experience",
                  ]}
                />
              </div>
              <Button className="w-full">
                <MessageSquare className="mr-2 h-4 w-4" />
                Generate Discussion Guide
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="edit" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Edit className="h-5 w-5" />
                Edit Discussion Guide
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {Object.entries(groupedQuestions).map(([topic, topicQuestions]) => (
                  <div key={topic} className="space-y-2">
                    <h3 className="text-lg font-semibold">{topic}</h3>
                    {topicQuestions.map((question) => (
                      <div key={question.id} className="flex items-center space-x-2">
                        <GripVertical className="h-5 w-5 text-muted-foreground" />
                        <Input
                          value={question.text}
                          onChange={(e) => updateQuestion(question.id, e.target.value)}
                          className="flex-grow"
                        />
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => toggleImportant(question.id)}
                        >
                          <Star className={`h-5 w-5 ${question.important ? 'text-yellow-400 fill-yellow-400' : 'text-muted-foreground'}`} />
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => removeQuestion(question.id)}
                        >
                          <Trash2 className="h-5 w-5 text-muted-foreground" />
                        </Button>
                      </div>
                    ))}
                    <Button onClick={() => addQuestion(topic)} variant="outline" size="sm">
                      <Plus className="mr-2 h-4 w-4" />
                      Add Question to {topic}
                    </Button>
                  </div>
                ))}
                <div className="pt-4">
                  <Button onClick={() => addQuestion("New Topic")} className="w-full">
                    <Plus className="mr-2 h-4 w-4" />
                    Add New Topic
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="logistics" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Demographics</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="age-range">Age Range</Label>
                  <AIPromptInput
                    placeholder="E.g., 25-40"
                    suggestions={["18-24", "25-34", "35-44", "45-54", "55+"]}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="location">Location</Label>
                  <AIPromptInput
                    placeholder="E.g., United States"
                    suggestions={["North America", "Europe", "Asia", "Global"]}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="race">Race/Ethnicity</Label>
                  <AIPromptInput
                    placeholder="E.g., Diverse mix"
                    suggestions={["Caucasian", "African American", "Hispanic", "Asian", "Mixed"]}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="income">Income Level</Label>
                  <AIPromptInput
                    placeholder="E.g., Middle income"
                    suggestions={["Low income", "Middle income", "High income", "Mixed"]}
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Screener Questions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {screenerQuestions.map((question, index) => (
                <div key={question.id} className="flex items-center space-x-2">
                  <Input
                    value={question.text}
                    onChange={(e) => {
                      const newQuestions = [...screenerQuestions]
                      newQuestions[index].text = e.target.value
                      setScreenerQuestions(newQuestions)
                    }}
                    className="flex-grow"
                  />
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => {
                      setScreenerQuestions(screenerQuestions.filter((_, i) => i !== index))
                    }}
                  >
                    <Trash2 className="h-5 w-5 text-muted-foreground" />
                  </Button>
                </div>
              ))}
              <Button onClick={() => setScreenerQuestions([...screenerQuestions, { id: Date.now(), text: "" }])}>
                <Plus className="mr-2 h-4 w-4" />
                Add Screener Question
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Screened Users</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Age</TableHead>
                    <TableHead>Gender</TableHead>
                    <TableHead>Income</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {screenedUsers.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell>{user.name}</TableCell>
                      <TableCell>{user.age}</TableCell>
                      <TableCell>{user.gender}</TableCell>
                      <TableCell>{user.income}</TableCell>
                      <TableCell>
                        <Button variant="ghost" size="sm">
                          View
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Final Participants</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Age</TableHead>
                    <TableHead>Gender</TableHead>
                    <TableHead>Income</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {finalUsers.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell>{user.name}</TableCell>
                      <TableCell>{user.age}</TableCell>
                      <TableCell>{user.gender}</TableCell>
                      <TableCell>{user.income}</TableCell>
                      <TableCell>
                        <Button variant="ghost" size="sm">
                          Remove
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="stimuli" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Upload Stimuli</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="stimulus-type">Stimulus Type</Label>
                  <Select>
                    <SelectTrigger id="stimulus-type">
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="image">Image</SelectItem>
                      <SelectItem value="video">Video</SelectItem>
                      <SelectItem value="audio">Audio</SelectItem>
                      <SelectItem value="document">Document</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="stimulus-name">Stimulus Name</Label>
                  <Input id="stimulus-name" placeholder="Enter name" />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="stimulus-description">Description</Label>
                <Textarea id="stimulus-description" placeholder="Enter description" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="stimulus-file">Upload File</Label>
                <Input id="stimulus-file" type="file" />
              </div>
              <Button className="w-full">
                <Upload className="mr-2 h-4 w-4" />
                Upload Stimulus
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Uploaded Stimuli</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Description</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow>
                    <TableCell>Homepage Mockup</TableCell>
                    <TableCell>Image</TableCell>
                    <TableCell>New homepage design for user feedback</TableCell>
                    <TableCell>
                      <Button variant="ghost" size="sm">
                        View
                      </Button>
                      <Button variant="ghost" size="sm">
                        Delete
                      </Button>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Product Demo</TableCell>
                    <TableCell>Video</TableCell>
                    <TableCell>Demonstration of new features</TableCell>
                    <TableCell>
                      <Button variant="ghost" size="sm">
                        View
                      </Button>
                      <Button variant="ghost" size="sm">
                        Delete
                      </Button>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="ai-interview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>AI Interview Setup</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="ai-persona">AI Interviewer Persona</Label>
                <Select>
                  <SelectTrigger id="ai-persona">
                    <SelectValue placeholder="Select persona" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="friendly">Friendly and Approachable</SelectItem>
                    <SelectItem value="professional">Professional and Formal</SelectItem>
                    <SelectItem value="casual">Casual and Relaxed</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="interview-style">Interview Style</Label>
                <Select>
                  <SelectTrigger id="interview-style">
                    <SelectValue placeholder="Select style" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="structured">Structured</SelectItem>
                    <SelectItem value="semi-structured">Semi-structured</SelectItem>
                    <SelectItem value="unstructured">Unstructured</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="follow-up">Follow-up Question Depth</Label>
                <Slider
                  id="follow-up"
                  min={1}
                  max={5}
                  step={1}
                  defaultValue={[3]}
                  className="w-full"
                />
              </div>
              <div className="flex items-center space-x-2">
                <Switch id="transcription" />
                <Label htmlFor="transcription">Enable Real-time Transcription</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Switch id="sentiment-analysis" />
                <Label htmlFor="sentiment-analysis">Enable Sentiment Analysis</Label>
              </div>
              <Button className="w-full">
                <Play className="mr-2 h-4 w-4" />
                Start AI Interview
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>AI Interview Results</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                AI interview results will be displayed here after conducting interviews.
              </p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      <div className="flex justify-end space-x-4">
        <Button variant="outline" onClick={onClose}>Cancel</Button>
        <Button>Create Study</Button>
      </div>
    </div>
  )
}