package com.test;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.*;

public class TestFuture {

    public static void main(String[] args) {
//        f1();
//        f2();
//        f3();
//        f4();
//        tt();
        ttt();

    }

    /**
     * FutureTask实现了两个接口，Runnable和Future，所以它既可以作为Runnable被线程执行，又可以作为Future得到Callable的返回值，
     * 那么这个组合的使用有什么好处呢？假设有一个很耗时的返回值需要计算，并且这个返回值不是立刻需要的话，那么就可以使用这个组合，
     * 用另一个线程去计算返回值，而当前线程在使用这个返回值之前可以做其它的操作，等到需要这个返回值时，再通过Future得到，岂不美哉
     **/
    static void f1() {
        Callable<Integer> callable = new Callable<Integer>() {
            public Integer call() throws Exception {
                return new Random().nextInt(100);
            }
        };
        FutureTask<Integer> future = new FutureTask<Integer>(callable);
        new Thread(future).start();
        try {
            Thread.sleep(5000);
            System.out.println("--------1----------" + future.get());
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
    }

    /**
     * ExecutorService继承自Executor，它的目的是为我们管理Thread对象，从而简化并发编程，Executor使我们无需显示的去管理线程的生命周期
     */
    static void f2() {
        ExecutorService threadPool = Executors.newSingleThreadExecutor();
        Future<Integer> future = threadPool.submit(new Callable<Integer>() {
            public Integer call() throws Exception {
                return new Random().nextInt(100);
            }
        });
        try {
            Thread.sleep(500);
            System.out.println("------2-----------" + future.get());
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        threadPool.shutdown();
    }

    /**
     * 其实也可以不使用CompletionService，可以先创建一个装Future类型的集合，用Executor提交的任务返回值添加到集合中，最后遍历集合取出数据，
     * 代码略。更新于2016-02-05，评论中就这个说法引发了讨论，其实是我没有讲清楚，抱歉。这里再阐述一下：
     * 提交到CompletionService中的Future是按照完成的顺序排列的，这种做法中Future是按照添加的顺序排列的。
     * 所以这两种方式的区别就像评论中fishjam所描述的那样。
     */
    static void f3() {
        ExecutorService threadPool = Executors.newCachedThreadPool();
        CompletionService<Integer> cs = new ExecutorCompletionService<Integer>(threadPool);
        for (int i = 1; i < 5; i++) {
            final int taskID = i;
            cs.submit(new Callable<Integer>() {
                public Integer call() throws Exception {
                    return taskID;
                }
            });
        }
        // 可能做一些事情
        for (int i = 1; i < 5; i++) {
            try {
                System.out.println(cs.take().get());
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        }

    }

    static void f4() {
        ExecutorService threadPool = Executors.newCachedThreadPool();
        List<Future<Integer>> ls = new ArrayList();
        for (int i = 1; i < 5; i++) {
            final int taskID = i;
            ls.add(threadPool.submit(new Callable<Integer>() {
                public Integer call() throws Exception {
                    return taskID;
                }
            }));
        }
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        for (Future<Integer> fu : ls) {
            try {
                System.out.println(fu.get());
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        }
        threadPool.shutdown();
    }

    /**
     * CountDownLatch是一个同步工具类，它允许一个或多个线程一直等待，直到其他线程的操作执行完后再执行。
     * 例如，应用程序的主线程希望在负责启动框架服务的线程已经启动所有的框架服务之后再执行。
     */
    static void tt() {
        // 进行首次查询（略），获取总页数
        int totalPage = 10;
        // 设置计数器，从0开始
        ExecutorService threadPool = Executors.newCachedThreadPool();
        final CountDownLatch countDownLatch = new CountDownLatch(totalPage - 1);
        // 定义Future数组，数组大小和计数器个数相同
        Future[] futures = new Future[totalPage];
        for (int i = 0; i < totalPage; i++) {
            // 将各个PageResult塞到线程池的各个线程里，返回Future数组
            final int flag = i;
            futures[i] = threadPool.submit(new Callable<String>() {
                // 返回取得的PageResult
                @Override
                public String call() throws Exception {
                    String result = "";
                    try {
                        Thread.sleep(50 * new Random().nextInt(100));
                        result = flag + "";
                        System.out.println(result);
                    } catch (Exception e) {
                        System.out.println(e);
                        throw e;
                    } finally {
                        // 线程完成任务后通过countDownLatch.countDown()来通知CountDownLatch对象，计数器-1
                        countDownLatch.countDown();
                    }
                    return result;
                }
            });
        }
        // 所有任务执行完毕后触发事件，唤醒await在latch上的主线程
        try {
            countDownLatch.await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        // 合并记录
        for (int j = 0; j < totalPage; j++) {
            try {
                if (futures[j] != null && futures[j].get() != null) {
                    System.out.println("j:  " + futures[j].get());
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        }
        threadPool.shutdown();
    }

    static void ttt() {
        // 进行首次查询（略），获取总页数
        int totalPage = 100;
        final CountDownLatch countDownLatch = new CountDownLatch(totalPage - 1);
        final ThreadPool tp = ThreadPool.getThreadPool(5);
        final int aa = 0;
        for (int i = 0; i < totalPage; i++) {
            // 将各个PageResult塞到线程池的各个线程里，返回Future数组
            System.out.println("---start-------" + i);
            final int flag = i;
            tp.execute(new Runnable() {
                @Override
                public void run() {
                    try {
                        Thread.sleep(50 * new Random().nextInt(100));
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    System.out.println(tp.toString() + "   flag  :  " + flag);
                    countDownLatch.countDown();
                }
            });
        }
        tp.destroy();
        System.out.println("-------end---------");
        // 所有任务执行完毕后触发事件，唤醒await在latch上的主线程
        try {
            countDownLatch.await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("-------end----end---------");

        // 合并记录
    }
}