import * as React from "react"
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
import {
  Brain,
  Calendar,
  DollarSign,
  Edit,
  Globe,
  GripVertical,
  Mail,
  MessageSquare,
  Mic,
  Plus,
  Star,
  Trash2,
  Upload,
  Users,
  Play,
} from "lucide-react"

interface Question {
  id: number
  text: string
  important: boolean
  topic: string
}

interface ScreenerQuestion {
  id: number
  text: string
}

interface User {
  id: number
  name: string
  age: number
  gender: string
  income: string
}

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
              <CommandItem
                key={index}
                onSelect={() => console.log(suggestion)}
              >
                {suggestion}
              </CommandItem>
            ))}
          </CommandGroup>
        </CommandList>
      </Command>
    </PopoverContent>
  </Popover>
)

export default function CreateStudy() {
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
    <div className="flex flex-col gap-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Create New Study</h1>
          <p className="text-sm text-muted-foreground">
            Set up your research study with AI assistance
          </p>
        </div>
        <Button>Save Draft</Button>
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
                    placeholder="E.g., All"
                    suggestions={["All", "Specific ethnic groups", "Diverse mix"]}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="income">Income Range</Label>
                  <AIPromptInput
                    placeholder="E.g., $50,000-$100,000"
                    suggestions={["Under $50,000", "$50,000-$100,000", "Over $100,000"]}
                  />
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <Switch id="in-person" />
                <Label htmlFor="in-person">In-person interviews</Label>
              </div>
              <div className="space-y-2">
                <Label>Demographic Statistics</Label>
                <div className="grid grid-cols-3 gap-4">
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-sm font-medium">Age Distribution</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">50/50</div>
                      <p className="text-xs text-muted-foreground">25-34 / 35-44</p>
                      <div className="mt-4 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div className="h-full bg-primary" style={{ width: '50%' }}></div>
                      </div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-sm font-medium">Gender Ratio</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">1:1</div>
                      <p className="text-xs text-muted-foreground">Male / Female</p>
                      <div className="mt-4 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div className="h-full bg-primary" style={{ width: '50%' }}></div>
                      </div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-sm font-medium">Income Level</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">50/50</div>
                      <p className="text-xs text-muted-foreground">Medium / High</p>
                      <div className="mt-4 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div className="h-full bg-primary" style={{ width: '50%' }}></div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <DollarSign className="h-5 w-5" />
                Compensation
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center space-x-2">
                <Input id="compensation" type="number" placeholder="Amount" />
                <Select>
                  <SelectTrigger id="compensation-type" className="w-[180px]">
                    <SelectValue placeholder="Type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="cash">Cash</SelectItem>
                    <SelectItem value="gift-card">Gift Card</SelectItem>
                    <SelectItem value="product">Product</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Mail className="h-5 w-5" />
                Email Template
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                placeholder="Enter your email template for participants here..."
                className="min-h-[200px]"
              />
              <div className="flex space-x-2">
                <Button variant="outline">
                  <Mail className="mr-2 h-4 w-4" />
                  Send via Outlook
                </Button>
                <Button variant="outline">
                  <Mail className="mr-2 h-4 w-4" />
                  Send via Gmail
                </Button>
                <Button variant="outline">
                  <Mail className="mr-2 h-4 w-4" />
                  Send via Yahoo
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Screener</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="screener-duration">Screener Call Duration (minutes)</Label>
                <Input id="screener-duration" type="number" defaultValue={15} />
              </div>
              <div className="space-y-2">
                <Label>Screener Questions</Label>
                {screenerQuestions.map((question, index) => (
                  <Input
                    key={question.id}
                    value={question.text}
                    onChange={(e) => {
                      const newQuestions = [...screenerQuestions]
                      newQuestions[index].text = e.target.value
                      setScreenerQuestions(newQuestions)
                    }}
                  />
                ))}
                <Button
                  onClick={() => setScreenerQuestions([...screenerQuestions, { id: Date.now(), text: "" }])}
                  variant="outline"
                >
                  <Plus className="mr-2 h-4 w-4" />
                  Add Screener Question
                </Button>
              </div>
              <div className="space-y-2">
                <Label>Screened Users</Label>
                <div className="border rounded-md p-2 space-y-2">
                  {screenedUsers.map((user) => (
                    <div key={user.id} className="flex justify-between items-center">
                      <span>{user.name} - {user.age} years old, {user.gender}, {user.income} income</span>
                      <Button variant="ghost" size="sm">Select</Button>
                    </div>
                  ))}
                </div>
              </div>
              <div className="space-y-2">
                <Label>Final Users for Interview</Label>
                <div className="border rounded-md p-2 space-y-2">
                  {finalUsers.map((user) => (
                    <div key={user.id} className="flex justify-between items-center">
                      <span>{user.name} - {user.age} years old, {user.gender}, {user.income} income</span>
                      <Button variant="ghost" size="sm">Remove</Button>
                    </div>
                  ))}
                </div>
              </div>
              <div className="space-y-2">
                <Label>Demographic Statistics</Label>
                <div className="grid grid-cols-3 gap-4">
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-sm font-medium">Age Distribution</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">50/50</div>
                      <p className="text-xs text-muted-foreground">25-34 / 35-44</p>
                      <div className="mt-4 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div className="h-full bg-primary" style={{ width: '50%' }}></div>
                      </div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-sm font-medium">Gender Ratio</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">1:1</div>
                      <p className="text-xs text-muted-foreground">Male / Female</p>
                      <div className="mt-4 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div className="h-full bg-primary" style={{ width: '50%' }}></div>
                      </div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-sm font-medium">Income Level</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">50/50</div>
                      <p className="text-xs text-muted-foreground">Medium / High</p>
                      <div className="mt-4 h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div className="h-full bg-primary" style={{ width: '50%' }}></div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="stimuli" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="h-5 w-5" />
                Upload Stimuli
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-center border-2 border-dashed rounded-lg p-12">
                <div className="text-center">
                  <Upload className="mx-auto h-12 w-12 text-muted-foreground" />
                  <p className="mt-2 text-sm text-muted-foreground">
                    Drag and drop or click to upload designs, prototypes, or other materials
                  </p>
                  <Button variant="secondary" className="mt-4">
                    Upload Files
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="ai-interview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Mic className="h-5 w-5" />
                AI Interview Demo
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <p className="text-sm text-muted-foreground">
                  This demo simulates how the AI voice chatbot will conduct the interview using the generated questions.
                </p>
                <div className="border rounded-lg p-4 space-y-2">
                  <p className="font-semibold">AI: Hello, thank you for participating in our study. Let's begin with the first question.</p>
                  {questions.map((question, index) => (
                    <div key={index} className="pl-4 border-l-2 border-gray-200">
                      <p className="font-semibold">AI: {question.text}</p>
                      <p className="text-sm text-muted-foreground italic">User response will be recorded here...</p>
                    </div>
                  ))}
                  <p className="font-semibold">AI: Thank you for your time and insights. Do you have any questions for me?</p>
                </div>
                <Button className="w-full">
                  <Play className="mr-2 h-4 w-4" />
                  Start AI Interview Demo
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}