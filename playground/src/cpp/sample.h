// SPDX-FileCopyrightText: 2023 Erin Catto
// SPDX-License-Identifier: MIT

#pragma once

#include "box2d/id.h"
#include "box2d/types.h"

// todo this include is slow
#include "enkiTS/TaskScheduler.h"

namespace pyb2d
{

    // namespace py = nanobind;

#define ARRAY_COUNT(A) (int) (sizeof(A) / sizeof(A[0]))

    struct Settings;

    class SampleTask : public enki::ITaskSet
    {
    public:

        SampleTask() = default;

        void ExecuteRange(enki::TaskSetPartition range, uint32_t threadIndex) override
        {
            m_task(range.start, range.end, threadIndex, m_taskContext);
        }

        b2TaskCallback* m_task = nullptr;
        void* m_taskContext = nullptr;
    };

    constexpr int32_t maxTasks = 64;
    constexpr int32_t maxThreads = 64;

    class Sample
    {
    public:

        explicit Sample(Settings& settings);
        virtual ~Sample();

        virtual void Step(Settings& settings);

        virtual void UpdateUI()
        {
        }

        virtual void Keyboard(int)
        {
        }

        virtual void MouseDown(b2Vec2 p, int button, int mod);
        virtual void MouseUp(b2Vec2 p, int button);
        virtual void MouseMove(b2Vec2 p);

        void ResetProfile();
        void ShiftOrigin(b2Vec2 newOrigin);

        friend class DestructionListener;
        friend class BoundaryListener;
        friend class ContactListener;

        void prepare_destruction();

        enki::TaskScheduler m_scheduler;
        SampleTask m_tasks[maxTasks];
        int32_t m_taskCount;
        int m_threadCount;

        b2BodyId m_groundBodyId;

        // DestructionListener m_destructionListener;
        int32_t m_textLine;
        b2WorldId m_worldId;
        b2JointId m_mouseJointId;
        int32_t m_stepCount;
        int32_t m_textIncrement;

        b2DebugDraw* p_debugDraw = nullptr;
    };

}  // namespace pyb2d
