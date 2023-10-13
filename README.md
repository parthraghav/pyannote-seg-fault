# pyannote-seg-fault

Minimum Reproducible Example (MRE) for pyannote/pyannote-audio/issues/1499

----

Hello,

I encountered a problem when trying to load the pretrained `pyannote/speaker-diarization-3.0` model from the **pyannote.audio** pipeline in the `rockylinux9/python3` environment. Specifically, I get a **Segmentation Fault (SIGSEGV)**. Interestingly, I can load the model successfully on my Mac M1.


**Environment:**

| | Version |
| -- | -- 
 | Python | 3.9 |
| OS / Docker Image | rockylinux:9.2.20230513 |
| pyannote-audio | 3.0.0 |
| torch | 2.1.0 |
| torchaudio | 2.1.0 |

```
(venv) sh-5.1# pip freeze | grep pyannote

pyannote.audio==3.0.0
pyannote.core==5.0.0
pyannote.database==5.0.1
pyannote.metrics==3.2.1
pyannote.pipeline==3.0.1
```

**Error Traceback:**

```
  torchaudio.set_audio_backend("soundfile")
Downloading (…)lve/main/config.yaml: 100%|█████████████████████████████████████████████████████████████████████| 467/467 [00:00<00:00, 10.5kB/s]
torchvision is not available - cannot save figures
Downloading pytorch_model.bin: 100%|███████████████████████████████████████████████████████████████████████| 5.91M/5.91M [00:00<00:00, 13.7MB/s]
Downloading (…)lve/main/config.yaml: 100%|█████████████████████████████████████████████████████████████████████| 399/399 [00:00<00:00, 67.1kB/s]
Fatal Python error: Segmentation fault

Thread 0x0000ffff940e1120 (most recent call first):
  File "/usr/lib64/python3.9/threading.py", line 316 in wait
  File "/usr/lib64/python3.9/threading.py", line 581 in wait
  File "/usr/local/lib/python3.9/site-packages/tqdm/_monitor.py", line 60 in run
  File "/usr/lib64/python3.9/threading.py", line 980 in _bootstrap_inner
  File "/usr/lib64/python3.9/threading.py", line 937 in _bootstrap

Current thread 0x0000ffff969cf020 (most recent call first):
  File "/usr/local/lib/python3.9/site-packages/asteroid_filterbanks/enc_dec.py", line 216 in multishape_conv1d
  File "/usr/local/lib/python3.9/site-packages/asteroid_filterbanks/scripting.py", line 37 in wrapper
  File "/usr/local/lib/python3.9/site-packages/asteroid_filterbanks/enc_dec.py", line 177 in forward
  File "/usr/local/lib64/python3.9/site-packages/torch/nn/modules/module.py", line 1527 in _call_impl
  File "/usr/local/lib64/python3.9/site-packages/torch/nn/modules/module.py", line 1518 in _wrapped_call_impl
  File "/usr/local/lib/python3.9/site-packages/pyannote/audio/models/blocks/sincnet.py", line 87 in forward
  File "/usr/local/lib64/python3.9/site-packages/torch/nn/modules/module.py", line 1527 in _call_impl
  File "/usr/local/lib64/python3.9/site-packages/torch/nn/modules/module.py", line 1518 in _wrapped_call_impl
  File "/usr/local/lib/python3.9/site-packages/pyannote/audio/models/segmentation/PyanNet.py", line 172 in forward
  File "/usr/local/lib64/python3.9/site-packages/torch/nn/modules/module.py", line 1527 in _call_impl
  File "/usr/local/lib64/python3.9/site-packages/torch/nn/modules/module.py", line 1518 in _wrapped_call_impl
  File "/usr/local/lib/python3.9/site-packages/pyannote/audio/core/model.py", line 195 in example_output
  File "/usr/lib64/python3.9/functools.py", line 993 in __get__
  File "/usr/local/lib/python3.9/site-packages/pyannote/audio/pipelines/speaker_diarization.py", line 148 in __init__
  File "/usr/local/lib/python3.9/site-packages/pyannote/audio/core/pipeline.py", line 136 in from_pretrained
  File "/app/audio.py", line 6 in <module>
Segmentation fault
```

**Code to Reproduce:**

```
import faulthandler
faulthandler.enable()
from pyannote.audio import Pipeline
from shared.utils import load_env

env = load_env()
# the following line throws a segmentation fault
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.0", use_auth_token=env["HF_ACCESS_TOKEN"])
```

To reproduce the bug:
1. Clone the [Docker Container - https://github.com/parthraghav/pyannote-seg-fault](https://github.com/parthraghav/pyannote-seg-fault) and `cd` into the cloned repo. 
2. Build the image by running `docker-compose up --no-start --build`.
3. Open the terminal in the GUI or using `docker exec -it [container_id_or_name] /bin/bash` cmd.
4. Run `python3 audio.py`

**GDB Backtrace**

```
(gdb) run audio.py
Starting program: /usr/bin/python3 audio.py
warning: Error disabling address space randomization: Operation not permitted
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
[New Thread 0xffff81407120 (LWP 234)]
[New Thread 0xffff7ebf7120 (LWP 235)]
[New Thread 0xffff7e3e7120 (LWP 236)]
[New Thread 0xffff6c455120 (LWP 237)]
[New Thread 0xffff69c45120 (LWP 238)]
[New Thread 0xffff67435120 (LWP 239)]
[Thread 0xffff67435120 (LWP 239) exited]
[Thread 0xffff69c45120 (LWP 238) exited]
[Thread 0xffff6c455120 (LWP 237) exited]
[Thread 0xffff7e3e7120 (LWP 236) exited]
[Thread 0xffff7ebf7120 (LWP 235) exited]
[Thread 0xffff81407120 (LWP 234) exited]
[Detaching after fork from child process 240]
[New Thread 0xffff7e3e7120 (LWP 241)]
[New Thread 0xffff7ebf7120 (LWP 242)]
[New Thread 0xffff81407120 (LWP 243)]
[Thread 0xffff81407120 (LWP 243) exited]
[Thread 0xffff7ebf7120 (LWP 242) exited]
[Thread 0xffff7e3e7120 (LWP 241) exited]
[Detaching after fork from child process 244]
/usr/local/lib/python3.9/site-packages/pyannote/audio/core/io.py:43: UserWarning: torchaudio._backend.set_audio_backend has been deprecated. With dispatcher enabled, this function is no-op. You can remove the function call.
  torchaudio.set_audio_backend("soundfile")
/usr/local/lib/python3.9/site-packages/torch_audiomentations/utils/io.py:27: UserWarning: torchaudio._backend.set_audio_backend has been deprecated. With dispatcher enabled, this function is no-op. You can remove the function call.
  torchaudio.set_audio_backend("soundfile")
torchvision is not available - cannot save figures
[New Thread 0xffff81407120 (LWP 245)]
[New Thread 0xffff7ebf7120 (LWP 246)]
[New Thread 0xffff7e3e7120 (LWP 247)]

Thread 1 "python3" received signal SIGSEGV, Segmentation fault.
0x0000ffff83940740 in __aarch64_cas4_acq () from /lib64/libc.so.6
(gdb) bt
#0  0x0000ffff83940740 in __aarch64_cas4_acq () from /lib64/libc.so.6
#1  0x0000ffff838c51f0 in readdir64 () from /lib64/libc.so.6
#2  0x0000ffff73a34bc4 in Xbyak_aarch64::util::Cpu::getFilePathMaxTailNumPlus1(char const*) ()
   from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#3  0x0000ffff73a34d5c in Xbyak_aarch64::util::Cpu::Cpu() () from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#4  0x0000ffff73ee6130 in dnnl::impl::cpu::aarch64::jit_sve_512_1x1_conv_kernel::init_conf(dnnl::impl::cpu::aarch64::jit_1x1_conv_conf_t&, dnnl::impl::convolution_desc_t const&, dnnl::impl::memory_desc_wrapper const&, dnnl::impl::memory_desc_wrapper const&, dnnl::impl::memory_desc_wrapper const&, dnnl_primitive_attr const&, int, bool) () from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#5  0x0000ffff73da0784 in dnnl_status_t dnnl::impl::primitive_desc_t::create<dnnl::impl::cpu::aarch64::jit_sve_512_1x1_convolution_fwd_t<(dnnl_data_type_t)3, (dnnl_data_type_t)3, (dnnl_data_type_t)3>::pd_t>(dnnl::impl::primitive_desc_t**, dnnl::impl::op_desc_t const*, dnnl_primitive_attr const*, dnnl_engine*, dnnl::impl::primitive_desc_t const*) () from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#6  0x0000ffff731d4e5c in dnnl::impl::primitive_desc_iterator_t::operator++() [clone .isra.0] ()
   from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#7  0x0000ffff731d575c in dnnl_primitive_desc::init() () from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#8  0x0000ffff731d6518 in dnnl::impl::primitive_desc_create(dnnl_primitive_desc**, dnnl_engine*, dnnl::impl::op_desc_t const*, dnnl_primitive_desc const*, dnnl_primitive_attr const*) () from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#9  0x0000ffff731ac014 in dnnl_convolution_forward_primitive_desc_create ()
   from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#10 0x0000ffff6ffb84bc in dnnl::convolution_forward::primitive_desc::primitive_desc(dnnl::engine const&, dnnl::prop_kind, dnnl::algorithm, dnnl::memory::desc const&, dnnl::memory::desc const&, dnnl::memory::desc const*, dnnl::memory::desc const&, std::vector<long, std::allocator<long> > const&, std::vector<long, std::allocator<long> > const*, std::vector<long, std::allocator<long> > const&, std::vector<long, std::allocator<long> > const&, dnnl::primitive_attr const&, bool) () from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#11 0x0000ffff70091824 in std::pair<dnnl::convolution_forward::primitive_desc, dnnl::convolution_forward> ideep::convolution_forward::get_primitive_desc<false>(ideep::tensor::desc const&, ideep::tensor::desc const&, ideep::tensor::desc const&, ideep::tensor::desc const&, std::vector<long, std::allocator<long> > const&, std::vector<long, std::allocator<long> > const&, std::vector<long, std::allocator<long> > const&, std::vector<long, std::allocator<long> > const&, unsigned long, bool, ideep::attr_t const&, dnnl::algorithm, dnnl::prop_kind, ideep::engine const&) [clone .isra.0] () from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#12 0x0000ffff700a20a8 in void ideep::convolution_forward::compute_dispatch<false, true, true>(ideep::tensor const&, ideep::tensor const&, ideep::tensor const&, std::vector<long, std::allocator<long> > const&, ideep::tensor&, std::vector<long, std::allocator<long> > const&, std::vector<long, std::allocator<long> > const&, std::vector<long, std::allocator<long> > const&, std::vector<long, std::allocator<long> > const&, int, bool, ideep::attr_t const&, dnnl::algorithm, dnnl::prop_kind, ideep::engine const&) ()
   from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#13 0x0000ffff70094318 in at::native::_mkldnn_convolution_out(at::Tensor const&, at::Tensor const&, at::Tensor const&, std::vector<long, std::allocator<long> >&, ideep::tensor&, c10::ArrayRef<long>, c10::ArrayRef<long>, c10::ArrayRef<long>, long, bool, ideep::attr_t const&) ()
   from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#14 0x0000ffff70094c04 in at::native::_mkldnn_convolution(at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<long>, c10::ArrayRef<long>, long, bool, c10::basic_string_view<char>, c10::List<c10::optional<c10::Scalar> >, c10::optional<c10::basic_string_view<char> >) () from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#15 0x0000ffff70095168 in at::native::mkldnn_convolution(at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<long>, c10::ArrayRef<long>, long) () from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#16 0x0000ffff7092cdd0 in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, c10::ArrayRef<long>, long), &at::(anonymous namespace)::(anonymous namespace)::wrapper_CompositeExplicitAutograd__mkldnn_convolution>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, c10::ArrayRef<long>, long> >, at::Tensor (at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, c10::ArrayRef<long>, long)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, at::Tensor const&, c10::optional--Type <RET> for more, q to quit, c to continue without paging--
<at::Tensor> const&, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, c10::ArrayRef<long>, long) ()
   from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#17 0x0000ffff701f9bec in at::_ops::mkldnn_convolution::call(at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, c10::ArrayRef<long>, long) () from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#18 0x0000ffff6fac82c8 in at::native::_convolution(at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<long>, c10::ArrayRef<long>, bool, c10::ArrayRef<long>, long, bool, bool, bool, bool) ()
   from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#19 0x0000ffff7092dfb0 in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, bool, c10::ArrayRef<c10::SymInt>, long, bool, bool, bool, bool), &at::(anonymous namespace)::(anonymous namespace)::wrapper_CompositeExplicitAutograd___convolution>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, bool, c10::ArrayRef<c10::SymInt>, long, bool, bool, bool, bool> >, at::Tensor (at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, bool, c10::ArrayRef<c10::SymInt>, long, bool, bool, bool, bool)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, bool, c10::ArrayRef<c10::SymInt>, long, bool, bool, bool, bool) () from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#20 0x0000ffff701e4a2c in at::_ops::_convolution::call(at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, bool, c10::ArrayRef<c10::SymInt>, long, bool, bool, bool, bool) ()
   from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#21 0x0000ffff6fabd4ec in at::native::convolution(at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<long>, c10::ArrayRef<long>, bool, c10::ArrayRef<long>, long) ()
   from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#22 0x0000ffff7092dc58 in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, bool, c10::ArrayRef<c10::SymInt>, long), &at::(anonymous namespace)::(anonymous namespace)::wrapper_CompositeExplicitAutograd__convolution>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, bool, c10::ArrayRef<c10::SymInt>, long> >, at::Tensor (at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, bool, c10::ArrayRef<c10::SymInt>, long)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, bool, c10::ArrayRef<c10::SymInt>, long) ()
   from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#23 0x0000ffff701e40c8 in at::_ops::convolution::call(at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, bool, c10::ArrayRef<c10::SymInt>, long) ()
   from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#24 0x0000ffff6fabef28 in at::native::conv1d_symint(at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, long) () from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#25 0x0000ffff70a990bc in c10::impl::wrap_kernel_functor_unboxed_<c10::impl::detail::WrapFunctionIntoFunctor_<c10::CompileTimeFunctionPointer<at::Tensor (at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, long), &at::(anonymous namespace)::(anonymous namespace)::wrapper_CompositeImplicitAutograd__conv1d>, at::Tensor, c10::guts::typelist::typelist<at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, long> >, at::Tensor (at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, long)>::call(c10::OperatorKernel*, c10::DispatchKeySet, at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, long) ()
   from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
#26 0x0000ffff705fdd2c in at::_ops::conv1d::call(at::Tensor const&, at::Tensor const&, c10::optional<at::Tensor> const&, c10::ArrayRef<long>, c10::ArrayRef<c10::SymInt>, c10::ArrayRef<long>, long) () from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_cpu.so
--Type <RET> for more, q to quit, c to continue without paging--
#27 0x0000ffff76c8314c in torch::autograd::THPVariable_conv1d(_object*, _object*, _object*) ()
   from /usr/local/lib64/python3.9/site-packages/torch/lib/libtorch_python.so
#28 0x0000ffff83a928f0 in cfunction_call () from /lib64/libpython3.9.so.1.0
#29 0x0000ffff83a80ddc in _PyObject_MakeTpCall () from /lib64/libpython3.9.so.1.0
#30 0x0000ffff83a7c830 in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#31 0x0000ffff83a76d10 in _PyEval_EvalCode () from /lib64/libpython3.9.so.1.0
#32 0x0000ffff83a86a78 in _PyFunction_Vectorcall () from /lib64/libpython3.9.so.1.0
#33 0x0000ffff83a9140c in PyVectorcall_Call () from /lib64/libpython3.9.so.1.0
#34 0x0000ffff83a7a438 in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#35 0x0000ffff83a76d10 in _PyEval_EvalCode () from /lib64/libpython3.9.so.1.0
#36 0x0000ffff83a86a78 in _PyFunction_Vectorcall () from /lib64/libpython3.9.so.1.0
#37 0x0000ffff83a78f48 in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#38 0x0000ffff83a86ce0 in function_code_fastcall () from /lib64/libpython3.9.so.1.0
#39 0x0000ffff83a90f54 in method_vectorcall () from /lib64/libpython3.9.so.1.0
#40 0x0000ffff83a7a438 in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#41 0x0000ffff83a76d10 in _PyEval_EvalCode () from /lib64/libpython3.9.so.1.0
#42 0x0000ffff83a869dc in _PyFunction_Vectorcall () from /lib64/libpython3.9.so.1.0
#43 0x0000ffff83a90f54 in method_vectorcall () from /lib64/libpython3.9.so.1.0
#44 0x0000ffff83a7a438 in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#45 0x0000ffff83a76d10 in _PyEval_EvalCode () from /lib64/libpython3.9.so.1.0
#46 0x0000ffff83a869dc in _PyFunction_Vectorcall () from /lib64/libpython3.9.so.1.0
#47 0x0000ffff83a80654 in _PyObject_FastCallDictTstate () from /lib64/libpython3.9.so.1.0
#48 0x0000ffff83a8eebc in _PyObject_Call_Prepend () from /lib64/libpython3.9.so.1.0
#49 0x0000ffff83b4f4f4 in slot_tp_call () from /lib64/libpython3.9.so.1.0
#50 0x0000ffff83a80d40 in _PyObject_MakeTpCall () from /lib64/libpython3.9.so.1.0
#51 0x0000ffff83a7bf6c in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#52 0x0000ffff83a86ce0 in function_code_fastcall () from /lib64/libpython3.9.so.1.0
#53 0x0000ffff83a90f54 in method_vectorcall () from /lib64/libpython3.9.so.1.0
#54 0x0000ffff83a7a438 in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#55 0x0000ffff83a76d10 in _PyEval_EvalCode () from /lib64/libpython3.9.so.1.0
#56 0x0000ffff83a869dc in _PyFunction_Vectorcall () from /lib64/libpython3.9.so.1.0
#57 0x0000ffff83a90f54 in method_vectorcall () from /lib64/libpython3.9.so.1.0
#58 0x0000ffff83a7a438 in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#59 0x0000ffff83a76d10 in _PyEval_EvalCode () from /lib64/libpython3.9.so.1.0
#60 0x0000ffff83a869dc in _PyFunction_Vectorcall () from /lib64/libpython3.9.so.1.0
#61 0x0000ffff83a80654 in _PyObject_FastCallDictTstate () from /lib64/libpython3.9.so.1.0
#62 0x0000ffff83a8eebc in _PyObject_Call_Prepend () from /lib64/libpython3.9.so.1.0
#63 0x0000ffff83b4f4f4 in slot_tp_call () from /lib64/libpython3.9.so.1.0
#64 0x0000ffff83a80d40 in _PyObject_MakeTpCall () from /lib64/libpython3.9.so.1.0
#65 0x0000ffff83a7c5e8 in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#66 0x0000ffff83a86ce0 in function_code_fastcall () from /lib64/libpython3.9.so.1.0
#67 0x0000ffff83a90f54 in method_vectorcall () from /lib64/libpython3.9.so.1.0
#68 0x0000ffff83a7a438 in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#69 0x0000ffff83a76d10 in _PyEval_EvalCode () from /lib64/libpython3.9.so.1.0
#70 0x0000ffff83a869dc in _PyFunction_Vectorcall () from /lib64/libpython3.9.so.1.0
#71 0x0000ffff83a90f54 in method_vectorcall () from /lib64/libpython3.9.so.1.0
--Type <RET> for more, q to quit, c to continue without paging--
#72 0x0000ffff83a7a438 in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#73 0x0000ffff83a76d10 in _PyEval_EvalCode () from /lib64/libpython3.9.so.1.0
#74 0x0000ffff83a869dc in _PyFunction_Vectorcall () from /lib64/libpython3.9.so.1.0
#75 0x0000ffff83a80654 in _PyObject_FastCallDictTstate () from /lib64/libpython3.9.so.1.0
#76 0x0000ffff83a8eebc in _PyObject_Call_Prepend () from /lib64/libpython3.9.so.1.0
#77 0x0000ffff83b4f4f4 in slot_tp_call () from /lib64/libpython3.9.so.1.0
#78 0x0000ffff83a80d40 in _PyObject_MakeTpCall () from /lib64/libpython3.9.so.1.0
#79 0x0000ffff83a7bf6c in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#80 0x0000ffff83a86ce0 in function_code_fastcall () from /lib64/libpython3.9.so.1.0
#81 0x0000ffff83a7c004 in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#82 0x0000ffff83a76d10 in _PyEval_EvalCode () from /lib64/libpython3.9.so.1.0
#83 0x0000ffff83a869dc in _PyFunction_Vectorcall () from /lib64/libpython3.9.so.1.0
#84 0x0000ffff83a860c0 in object_vacall () from /lib64/libpython3.9.so.1.0
#85 0x0000ffff83b08328 in PyObject_CallFunctionObjArgs () from /lib64/libpython3.9.so.1.0
#86 0x0000ffff83a8579c in _PyObject_GenericGetAttrWithDict () from /lib64/libpython3.9.so.1.0
#87 0x0000ffff83ad96d4 in slot_tp_getattr_hook () from /lib64/libpython3.9.so.1.0
#88 0x0000ffff83a7853c in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#89 0x0000ffff83a76d10 in _PyEval_EvalCode () from /lib64/libpython3.9.so.1.0
#90 0x0000ffff83a86a78 in _PyFunction_Vectorcall () from /lib64/libpython3.9.so.1.0
#91 0x0000ffff83a806c8 in _PyObject_FastCallDictTstate () from /lib64/libpython3.9.so.1.0
#92 0x0000ffff83a8eba0 in slot_tp_init () from /lib64/libpython3.9.so.1.0
#93 0x0000ffff83a81048 in type_call () from /lib64/libpython3.9.so.1.0
#94 0x0000ffff83a912f0 in _PyObject_Call () from /lib64/libpython3.9.so.1.0
#95 0x0000ffff83a7a438 in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#96 0x0000ffff83a76d10 in _PyEval_EvalCode () from /lib64/libpython3.9.so.1.0
#97 0x0000ffff83a86a78 in _PyFunction_Vectorcall () from /lib64/libpython3.9.so.1.0
#98 0x0000ffff83a90eb0 in method_vectorcall () from /lib64/libpython3.9.so.1.0
#99 0x0000ffff83a78f48 in _PyEval_EvalFrameDefault () from /lib64/libpython3.9.so.1.0
#100 0x0000ffff83a76d10 in _PyEval_EvalCode () from /lib64/libpython3.9.so.1.0
#101 0x0000ffff83b06494 in _PyEval_EvalCodeWithName () from /lib64/libpython3.9.so.1.0
#102 0x0000ffff83b06420 in PyEval_EvalCodeEx () from /lib64/libpython3.9.so.1.0
#103 0x0000ffff83b063d0 in PyEval_EvalCode () from /lib64/libpython3.9.so.1.0
#104 0x0000ffff83b43fac in run_eval_code_obj () from /lib64/libpython3.9.so.1.0
#105 0x0000ffff83b3e568 in run_mod () from /lib64/libpython3.9.so.1.0
#106 0x0000ffff83b374cc in pyrun_file () from /lib64/libpython3.9.so.1.0
#107 0x0000ffff83b36c3c in PyRun_SimpleFileExFlags () from /lib64/libpython3.9.so.1.0
#108 0x0000ffff83b325a8 in Py_RunMain () from /lib64/libpython3.9.so.1.0
#109 0x0000ffff83af4528 in Py_BytesMain () from /lib64/libpython3.9.so.1.0
#110 0x0000ffff8383c79c in __libc_start_call_main () from /lib64/libc.so.6
#111 0x0000ffff8383c86c in __libc_start_main_impl () from /lib64/libc.so.6
#112 0x0000aaaad18a0830 in _start ()
```
