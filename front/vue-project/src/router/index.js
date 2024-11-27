import {createRouter, createWebHistory} from 'vue-router'
import Home from '@/views/Home.vue'
import Resume from "@/views/Resume.vue"
import Center from "@/views/Center.vue"
import WorkPublish from "@/views/WorkPublish";
import Manager from '@/views/Manager.vue'
import WorkCenter from "@/views/WorkCenter";
import Pool from "@/views/Pool";
import Invite from "@/views/Invite";
import Personnel from "@/views/Personnel";
import StudentJob from "@/views/StudentJob";
import SchoolManager from "@/views/SchoolManager";
import UserManager from "@/views/UserManager";
import ClassManager from "@/views/ClassManager";
import TeacherClass from "@/views/TeacherClass";
import WorkAnalysis from "@/views/WorkAnalysis";
import ClassDetails from "@/views/ClassDetails"

const routes = [
    {path: "/:date?", component: Home, name: 'home'},
    {path: '/resume/:account', component: Resume, name: "resume"},
    {path: "/personnel/:date?", component: Personnel, name: "personnel"},
    {path: "/workAnalysis/:date?", component: WorkAnalysis, name: 'workAnalysis'},
    {path: "/classDetails/:date?", component: ClassDetails, name: 'classDetails'},
    {
        path: '/work',
        children: [
            {
                path: 'workPublish/:date?',
                component: WorkPublish,
                name: 'workPublish'
            },
            {
                path: "workCenter/:date?",
                component: WorkCenter,
                name: "workCenter"
            },
            {
                path: "workDetails/:id",
                component: WorkPublish,
                name: "workDetails"
            }
        ]
    },
    {
        path: "/user",
        children: [
            {path: "center/:date?", component: Center, name: 'center'},
            {path: "manager/:date?", component: Manager, name: 'manager'},
            {path: 'pool/:date?', component: Pool, name: "pool"},
            {path: 'invite/:date?', component: Invite, name: "invite"},
            {path: "job/:date?", component: StudentJob, name: "job"},
            {path: 'class/:date?', component: TeacherClass, name: "class"}
        ]
    },
    {
        path: "/school",
        children: [
            {
                path: "schoolManager/:date?",
                component: SchoolManager,
                name: 'schoolManager'
            },
            {
                path: "classManager/:date?",
                component: ClassManager,
                name: 'classManager'
            },
        ]
    },
    {
        path: '/userManager/:date?', component: UserManager, name: 'userManager'
    }
]

const router = createRouter({
    history: createWebHistory("/"),
    routes
})

export default router