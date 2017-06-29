# BSP support for Sparc/Leon
from build_rts_support import readfile
from build_rts_support.bsp import BSP
from build_rts_support.target import DFBBTarget


class LeonArch(BSP):
    @property
    def name(self):
        return "leon"

    def __init__(self):
        super(LeonArch, self).__init__()
        self.add_linker_switch('-Wl,-u_start', loader=None)
        self.add_sources('arch', [
            'sparc/leon/crt0.S',
            'sparc/leon/hw_init.S',
            'sparc/src/sparc.h',
            'src/s-macres/leon/s-macres.adb'])
        self.add_sources('gnarl', [
            'src/s-bbcppr/old/s-bbcppr.ads',
            'src/s-bbcppr/sparc/s-bbcppr.adb',
            'src/s-bbcppr/sparc/s-bcpith.adb',
            'src/s-bbcpsp/leon/s-bbcpsp.ads',
            'sparc/src/context_switch.S',
            'sparc/src/trap_handler.S',
            'sparc/src/interrupt_masking.S',
            'sparc/src/floating_point.S',
            'src/s-bbcaco/s-bbcaco.ads',
            'src/s-bbcaco/leon/s-bbcaco.adb',
            'src/s-bbinte/generic/s-bbinte.adb'])


class LeonTarget(DFBBTarget):
    @property
    def has_newlib(self):
        return True

    @property
    def zfp_system_ads(self):
        return 'system-xi-sparc.ads'

    @property
    def sfp_system_ads(self):
        return 'system-xi-sparc-ravenscar.ads'

    @property
    def full_system_ads(self):
        return 'system-xi-sparc-full.ads'

    def __init__(self):
        super(LeonTarget, self).__init__(
            mem_routines=True,
            small_mem=False)

    def amend_rts(self, rts_profile, conf):
        super(LeonTarget, self).amend_rts(rts_profile, conf)
        conf.rts_xml = \
            conf.rts_xml.replace(
                ' "-nolibc",', '')
        if rts_profile == 'ravenscar-full':
            # Use leon-zcx.specs to link with -lc.
            conf.config_files.update(
                {'link-zcx.spec': readfile('sparc/leon/leon-zcx.specs')})
            conf.rts_xml = conf.rts_xml.replace(
                '"-nostartfiles",',
                '"--specs=${RUNTIME_DIR(ada)}/link-zcx.spec",')


class Leon2(LeonTarget):
    @property
    def name(self):
        return "leon"

    @property
    def target(self):
        return 'leon-elf'

    @property
    def parent(self):
        return LeonArch

    @property
    def c_switches(self):
        # The required compiler switches
        return ('-DLEON', '-DLEON2')

    def __init__(self):
        super(Leon2, self).__init__()

        self.add_linker_script('sparc/leon/leon.ld', loader=None)
        self.add_sources('crt0', [
            'src/s-textio/leon/s-textio.adb',
            'src/s-bbbopa/leon/s-bbbopa.ads'])
        self.add_sources('gnarl', [
            'src/s-bbsumu/generic/s-bbsumu.adb',
            'src/s-bbbosu/leon/s-bbsule.ads',
            'src/s-bbbosu/leon/s-bbbosu.adb',
            'src/s-bbpara/leon/s-bbpara.ads',
            'src/a-intnam/leon/a-intnam.ads'])


class Leon3(LeonTarget):
    @property
    def name(self):
        return "leon3"

    @property
    def target(self):
        return 'leon3-elf'

    @property
    def parent(self):
        return LeonArch

    @property
    def need_fix_ut699(self):
        return True

    @property
    def c_switches(self):
        # The required compiler switches
        res = ('-DLEON', '-DLEON3')
        if self.need_fix_ut699:
            res += ('-DFIX_UT699',)
        return res

    @property
    def compiler_switches(self):
        if self.need_fix_ut699:
            return ('-mfix-ut699',)
        return ()

    @property
    def has_single_precision_fpu(self):
        # Single precision sqrt is buggy on UT699
        return not self.need_fix_ut699

    @property
    def readme_file(self):
        return 'sparc/leon3/README'

    def __init__(self):
        super(Leon3, self).__init__()

        self.add_linker_script('sparc/leon3/leon.ld', loader=None)
        self.add_sources('crt0', [
            'src/s-textio/leon3/s-textio.adb',
            'src/s-bbbopa/leon3/s-bbbopa.ads'])
        self.add_sources('gnat', [
            'src/i-leon3.ads',
            'src/i-leon3-uart.ads',
            'src/i-leon3-cache.ads'])
        self.add_sources('gnarl', [
            'src/i-leon3-timers.ads',
            'src/i-leon3-irqmp.ads',
            'src/s-bbbosu/leon3/s-bbbosu.adb',
            'src/s-bbpara/leon/s-bbpara.ads',
            'src/a-intnam/leon3/a-intnam.ads'])


class Leon4(Leon3):
    @property
    def name(self):
        return "leon4"

    def __init__(self):
        super(Leon4, self).__init__()
        self.update_pair('s-bbbopa.ads', 'src/s-bbbopa/leon4/s-bbbopa.ads')
